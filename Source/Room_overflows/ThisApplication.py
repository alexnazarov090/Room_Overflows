#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(path)
import System
import clr
clr.AddReference("RevitAPI.dll")
clr.AddReference("RevitAPIUI.dll")
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
from System import Array
from System.Threading import ThreadStart, Thread, ApartmentState
from System.ComponentModel import BackgroundWorker
import System.Drawing
import System.Windows.Forms as WinForms
from Autodesk.Revit import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Macros import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Category
from Autodesk.Revit.UI.Selection import *
import math
import re


class ThisApplication (ApplicationEntryPoint):
    #region Revit Macros generated code
    def FinishInitialization(self):
        ApplicationEntryPoint.FinishInitialization(self)
        self.InternalStartup()
    
    def OnShutdown(self):
        self.InternalShutdown()
        ApplicationEntryPoint.OnShutdown(self)
    
    def InternalStartup(self):
        self.Startup()
    
    def InternalShutdown(self):
        self.Shutdown()
    #endregion
    
    def Startup(self):
        self
        
    def Shutdown(self):
        self
        
    
    # Transaction mode
    def GetTransactionMode(self):
        return Attributes.TransactionMode.Manual
    
    # Addin Id
    def GetAddInId(self):
        return '7041D847-82F3-4589-805B-A2C5B88483B5'

    def room_overflows(self):

        # Initialize the form
        main_form = MainForm(self)
        # Define our new Windows.Forms.Application.object
        win_form_app = WinForms.Application
        # Run our MainForm
        win_form_app.Run(main_form)


class CalculateRoomOverflows(object):
    def __init__(self, rvt_doc, space_id_par,  pressure_cls_par, 
                overflow_par, inflow_par, door_crack_width=0.001, flow_coefficient=0.7):
        self.doc = rvt_doc
        self.uidoc = UIDocument(self.doc)
        self.space_id_par = space_id_par
        self.pressure_cls_par = pressure_cls_par
        self.overflow_par = overflow_par
        self.inflow_par = inflow_par
        self.door_crack_width = door_crack_width
        self.flow_coefficient = flow_coefficient
        self._worker = BackgroundWorker()
        self.CalcStart = Event()
        self.ReportProgress = Event()
        self.CalcEnd = Event()
        self._worker.DoWork += lambda _, __: self.__main()
        #self._worker.ProgressChanged += self.__worker_ProgressChanged
        self._worker.RunWorkerCompleted += lambda _, __: self.CalcEnd.emit()
        #self._worker.WorkerReportsProgress = True
        #self._worker.WorkerSupportsCancellation = True

    def main(self):
        try:
            sel = self.uidoc.Selection
            ref = sel.PickObject(ObjectType.Element, "Please pick a linked model instance")
            rvt_link = self.doc.GetElement(ref.ElementId)
            self.linkedDoc = rvt_link.GetLinkDocument()

            self.doors = FilteredElementCollector(self.linkedDoc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_Doors).ToElements()
            self.spaces = FilteredElementCollector(self.doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_MEPSpaces).ToElements()
            self.CalcStart.emit(len(self.doors) + 2*(len(self.spaces)))
            self.__main()
            self.CalcEnd.emit()
            
        except:
            WinForms.MessageBox.Show("Error in obtaining linked model", "Error!", WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Error)
            return

    #def mainAsync(self):
    #    sel = self.uidoc.Selection
    #    ref = sel.PickObject(ObjectType.Element, "Please pick a linked model instance")
    #    rvt_link = self.doc.GetElement(ref.ElementId)
    #    self.linkedDoc = rvt_link.GetLinkDocument()
    #    self.doors = FilteredElementCollector(self.linkedDoc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_Doors).ToElements()
    #    self.spaces = FilteredElementCollector(self.doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_MEPSpaces).ToElements()
    #    
    #    if not self._worker.IsBusy:
    #        self.CalcStart.emit(len(self.doors) + 2*(len(self.spaces)))
    #        self._worker.RunWorkerAsync()

    #def __worker_ProgressChanged(self, sender, args):
    #    self.CalcStart.emit(args.ProgressPercentage)

    def __main(self):
        with TransactionGroup(self.doc, 'Calculate Room Overflows') as tg:
            tg.Start()

            try:
                self.spaces_data = {space.get_Parameter(self.space_id_par).AsString():space for space in self.spaces}
            except:
                WinForms.MessageBox.Show("Task failed!", "Error!", WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Error)
                return

            with Transaction(self.doc, 'Reset overflow/inflow values') as tr:
                tr.Start()
                self.reset_overflows(self.spaces)
                tr.Commit()

            overflows_data = {}
            inflows_data = {}
            phases = self.linkedDoc.Phases
            phase = phases[phases.Size - 1]
            counter = 0

            for door in self.doors:
                try:
                    room1 = door.FromRoom[phase]
                    room2 = door.ToRoom[phase]
                    if room1 and room2:
                        airflow, overflow_space, inflow_space = self.calculate_overflow(door, (room1, room2), self.spaces_data)
                        overflows_data[overflow_space] = overflows_data.get(overflow_space, 0) + airflow
                        inflows_data[inflow_space] = inflows_data.get(inflow_space, 0) + airflow

                except Exception as e:
                    pass

                counter += 1
                self.ReportProgress.emit(counter)
                #self._worker.ReportProgress(counter)

            with Transaction(self.doc, "Set overflows") as tr:
                tr.Start()
                try:
                    for overflow_space, overflow in overflows_data.items():
                    
                        room_overflow_par = overflow_space.get_Parameter(self.overflow_par)
                        conv_val = UnitUtils.ConvertToInternalUnits(overflow, DisplayUnitType.DUT_CUBIC_METERS_PER_HOUR)
                        room_overflow_par.Set(conv_val)
                        counter += 1
                        self.ReportProgress.emit(counter)

                    for inflow_space, inflow in inflows_data.items():
                    
                        room_inflow_par = inflow_space.get_Parameter(self.inflow_par)
                        conv_val = UnitUtils.ConvertToInternalUnits(inflow, DisplayUnitType.DUT_CUBIC_METERS_PER_HOUR)
                        room_inflow_par.Set(conv_val)
                        counter += 1
                        self.ReportProgress.emit(counter)

                except Exception as e:
                    TaskDialog.Show("Error in setting airflow values", str(e))
                tr.Commit()

            commit_status = tg.Assimilate()

            if commit_status != TransactionStatus.Committed: 
                WinForms.MessageBox.Show("Task failed!", "Error!", 
                WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Error)
    
    def calculate_overflow(self, door, rooms, spaces_data):
        door_width = float(door.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsValueString())
        door_height = float(door.get_Parameter(BuiltInParameter.DOOR_HEIGHT).AsValueString())
        
        if door_width == 0 and door_height == 0:
            door_width = float(door.Symbol.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsValueString())
            door_height = float(door.Symbol.get_Parameter(BuiltInParameter.DOOR_HEIGHT).AsValueString())

        if door_width < 1300:
            door_crack_area = (2*(door_width/1000 + door_height/1000))*self.door_crack_width
        else:
            door_crack_area = (2*(door_width/1000 + door_height/1000) + door_height/1000)*self.door_crack_width
        
        mu = float(self.flow_coefficient)
        room_pressures = {}

        for room in rooms:
            space = self.spaces_data[room.UniqueId]
            room_pressure = space.get_Parameter(self.pressure_cls_par).AsString()
            
            if room_pressure:
                match = re.search(r"[+]?(-?\d+)", room_pressure)
                if match:
                    room_pressures[space] = (int(match.group(1)))
                else:
                    room_pressures[space] = 0
            else:
                room_pressures[space] = 0

        sorted_spaces = sorted(room_pressures.items(), key=lambda x: x[1], reverse=True)
        
        P1 = sorted_spaces[0][1]
        P2 = sorted_spaces[1][1]
        dP = P1 - P2
        
        # dP = (max(room_pressures) - room_pressures[0]) + (max(room_pressures) - room_pressures[1])
        dL = 3600*door_crack_area*mu*math.sqrt((2*dP)/1.2)
        
        return dL, sorted_spaces[0][0], sorted_spaces[1][0]

    def reset_overflows(self, spaces):
        for space in spaces:
            try:
                overflow_par = space.get_Parameter(self.overflow_par)
                overflow_par.Set(0)
            except Exception as e:
                TaskDialog.Show("Error in resetting overflow", str(e))
            
            try:
                inflow_par = space.get_Parameter(self.inflow_par)
                inflow_par.Set(0)
            except Exception as e:
                TaskDialog.Show("Error in resetting inflow", str(e))  


class MainForm(WinForms.Form):
    def __init__(self, __revit__):
        self.app = __revit__.Application
        self.doc = __revit__.ActiveUIDocument.Document
        self.parameters = {}
        self.InitializeComponent()

    def InitializeComponent(self):
        """Initialize form components."""
        self.components = System.ComponentModel.Container()
        self.tableLayoutPanel = WinForms.TableLayoutPanel()
        self.shared_parameters_label = WinForms.Label()
        self.space_id_par_label = WinForms.Label()
        self.pressure_cls_par_label = WinForms.Label()
        self.overflow_par_label = WinForms.Label()
        self.inflow_par_label = WinForms.Label()
        self.launch_label = WinForms.Label()
        self.shared_parameters_comboBox = WinForms.ComboBox()
        self.space_id_par_comboBox = WinForms.ComboBox()
        self.pressure_cls_par_comboBox = WinForms.ComboBox()
        self.overflow_par_comboBox = WinForms.ComboBox()
        self.inflow_par_comboBox = WinForms.ComboBox()
        self.run_button = WinForms.Button()
        self.pars_set_groupBox = WinForms.GroupBox()
        self.shr_pars_radio_button = WinForms.RadioButton()
        self.prj_pars_radio_button = WinForms.RadioButton()
        self.door_pars_groupBox = WinForms.GroupBox()
        self.door_crack_width_textBox = System.Windows.Forms.TextBox()
        self.flow_coeff_textBox = System.Windows.Forms.TextBox()
        self.door_crack_width_label = System.Windows.Forms.Label()
        self.flow_coeff_label = System.Windows.Forms.Label()
        self.space_id_par_textBox = System.Windows.Forms.TextBox()
        self.pressure_cls_par_textBox = System.Windows.Forms.TextBox()
        self.overflow_par_textBox = System.Windows.Forms.TextBox()
        self.inflow_par_textBox = System.Windows.Forms.TextBox()
        self.progressBar = System.Windows.Forms.ProgressBar()
        self.Shown += self.On_MainForm_StartUp
        self.FormClosing += self.On_MainForm_Closing
        self.pars_set_groupBox.SuspendLayout()
        self.door_pars_groupBox.SuspendLayout()
        self.tableLayoutPanel.SuspendLayout()
        self.SuspendLayout()
        #
        # table_layout
        #
        self.tableLayoutPanel.Anchor = WinForms.AnchorStyles.Top | WinForms.AnchorStyles.Bottom | WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
        self.tableLayoutPanel.BackColor = System.Drawing.SystemColors.Control
        self.tableLayoutPanel.CellBorderStyle = WinForms.TableLayoutPanelCellBorderStyle.Inset
        self.tableLayoutPanel.ColumnCount = 2
        self.tableLayoutPanel.ColumnStyles.Add(WinForms.ColumnStyle(WinForms.SizeType.Percent, 50))
        self.tableLayoutPanel.ColumnStyles.Add(WinForms.ColumnStyle(WinForms.SizeType.Percent, 50))
        self.tableLayoutPanel.Controls.Add(self.shared_parameters_label, 0, 0)
        self.tableLayoutPanel.Controls.Add(self.space_id_par_label, 0, 1)        
        self.tableLayoutPanel.Controls.Add(self.pressure_cls_par_label, 0, 3)
        self.tableLayoutPanel.Controls.Add(self.overflow_par_label, 0, 5)
        self.tableLayoutPanel.Controls.Add(self.inflow_par_label, 0, 7)
        self.tableLayoutPanel.Controls.Add(self.launch_label, 0, 9)
        self.tableLayoutPanel.Controls.Add(self.space_id_par_textBox, 1, 2)
        self.tableLayoutPanel.Controls.Add(self.pressure_cls_par_textBox, 1, 4)
        self.tableLayoutPanel.Controls.Add(self.overflow_par_textBox, 1, 6)
        self.tableLayoutPanel.Controls.Add(self.inflow_par_textBox, 1, 8)
        self.tableLayoutPanel.Controls.Add(self.shared_parameters_comboBox, 1, 0)
        self.tableLayoutPanel.Controls.Add(self.space_id_par_comboBox, 1, 1)
        self.tableLayoutPanel.Controls.Add(self.pressure_cls_par_comboBox, 1, 3)
        self.tableLayoutPanel.Controls.Add(self.overflow_par_comboBox, 1, 5)
        self.tableLayoutPanel.Controls.Add(self.inflow_par_comboBox, 1, 7)
        self.tableLayoutPanel.Controls.Add(self.run_button, 1, 9)
        self.tableLayoutPanel.Location = System.Drawing.Point(12, 141)
        self.tableLayoutPanel.Name = "tableLayoutPanel"
        self.tableLayoutPanel.RowCount = 10
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.RowStyles.Add(WinForms.RowStyle(WinForms.SizeType.Percent, 10))
        self.tableLayoutPanel.Size = System.Drawing.Size(576, 369)
        self.tableLayoutPanel.TabIndex = 0
        # 
        # pars_set_groupBox
        # 
        self.pars_set_groupBox.Anchor = WinForms.AnchorStyles.Top | WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
        self.pars_set_groupBox.Controls.Add(self.shr_pars_radio_button)
        self.pars_set_groupBox.Controls.Add(self.prj_pars_radio_button)
        self.pars_set_groupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.pars_set_groupBox.Location = System.Drawing.Point(12, 12)
        self.pars_set_groupBox.Name = "pars_set_groupBox"
        self.pars_set_groupBox.Size = System.Drawing.Size(379, 90)
        self.pars_set_groupBox.TabIndex = 1
        self.pars_set_groupBox.TabStop = False
        self.pars_set_groupBox.Text = "Choose Parameter Set"
        # 
        # prj_pars_radio_button
        # 
        self.prj_pars_radio_button.Anchor = WinForms.AnchorStyles.Top | WinForms.AnchorStyles.Bottom | WinForms.AnchorStyles.Left
        self.prj_pars_radio_button.Checked = True
        self.prj_pars_radio_button.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.prj_pars_radio_button.Location = System.Drawing.Point(28, 30)
        self.prj_pars_radio_button.Name = "prj_pars_radio_button"
        self.prj_pars_radio_button.Size = System.Drawing.Size(150, 44)
        self.prj_pars_radio_button.TabIndex = 0
        self.prj_pars_radio_button.TabStop = True
        self.prj_pars_radio_button.Text = "Project Parameters"
        self.prj_pars_radio_button.UseVisualStyleBackColor = True
        self.prj_pars_radio_button.CheckedChanged += self.prj_pars_radio_button_CheckChng
        # 
        # shr_pars_radio_button 
        # 
        self.shr_pars_radio_button.Anchor = WinForms.AnchorStyles.Top | WinForms.AnchorStyles.Bottom | WinForms.AnchorStyles.Right
        self.shr_pars_radio_button.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.shr_pars_radio_button.Location = System.Drawing.Point(207, 30)
        self.shr_pars_radio_button.Name = "shr_pars_radio_button"
        self.shr_pars_radio_button.Size = System.Drawing.Size(150, 44)
        self.shr_pars_radio_button.TabIndex = 1
        self.shr_pars_radio_button.TabStop = True
        self.shr_pars_radio_button.Text = "Shared Parameters"
        self.shr_pars_radio_button.UseVisualStyleBackColor = True
        self.shr_pars_radio_button.CheckedChanged += self.shr_pars_radio_button_CheckChng
        # 
        # door_pars_groupBox
        # 
        self.door_pars_groupBox.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right
        self.door_pars_groupBox.Controls.Add(self.flow_coeff_textBox)
        self.door_pars_groupBox.Controls.Add(self.flow_coeff_label)
        self.door_pars_groupBox.Controls.Add(self.door_crack_width_textBox)
        self.door_pars_groupBox.Controls.Add(self.door_crack_width_label)
        self.door_pars_groupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.door_pars_groupBox.Location = System.Drawing.Point(397, 12)
        self.door_pars_groupBox.Name = "door_pars_groupBox"
        self.door_pars_groupBox.Size = System.Drawing.Size(191, 90)
        self.door_pars_groupBox.TabIndex = 2
        self.door_pars_groupBox.TabStop = False
        self.door_pars_groupBox.Text = "Door Parameters"
        # 
        # door_crack_width_label
        # 
        self.door_crack_width_label.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left
        self.door_crack_width_label.AutoSize = True
        self.door_crack_width_label.Location = System.Drawing.Point(7, 22)
        self.door_crack_width_label.Name = "door_crack_width_label"
        self.door_crack_width_label.Size = System.Drawing.Size(108, 16)
        self.door_crack_width_label.TabIndex = 0
        self.door_crack_width_label.Text = "Door Crack Width"
        # 
        # door_crack_width_textBox
        # 
        self.door_crack_width_textBox.Location = System.Drawing.Point(139, 22)
        self.door_crack_width_textBox.Name = "door_crack_width_textBox"
        self.door_crack_width_textBox.Size = System.Drawing.Size(46, 22)
        self.door_crack_width_textBox.TabIndex = 1
        self.door_crack_width_textBox.Text = "0.001"
        # 
        # flow_coeff_label
        # 
        self.flow_coeff_label.AutoSize = True
        self.flow_coeff_label.Location = System.Drawing.Point(7, 57)
        self.flow_coeff_label.Name = "flow_coeff_label"
        self.flow_coeff_label.Size = System.Drawing.Size(119, 16)
        self.flow_coeff_label.TabIndex = 2
        self.flow_coeff_label.Text = "Flow Coefficient (μ)"
        # 
        # flow_coeff_textBox
        # 
        self.flow_coeff_textBox.Location = System.Drawing.Point(139, 57)
        self.flow_coeff_textBox.Name = "flow_coeff_textBox"
        self.flow_coeff_textBox.Size = System.Drawing.Size(46, 22)
        self.flow_coeff_textBox.TabIndex = 3
        self.flow_coeff_textBox.Text = "0.7"
        # 
        # shared_parameters_label
        # 
        self.shared_parameters_label.Anchor = WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
        self.shared_parameters_label.AutoSize = True
        self.shared_parameters_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.shared_parameters_label.Location = System.Drawing.Point(5, 7)
        self.shared_parameters_label.Name = "shared_parameters_label"
        self.shared_parameters_label.Size = System.Drawing.Size(279, 20)
        self.shared_parameters_label.TabIndex = 10
        self.shared_parameters_label.Text = "Shared Parameters Group"
        self.shared_parameters_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        # 
        # shared_parameters_comboBox
        # 
        self.shared_parameters_comboBox.Anchor = WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
        self.shared_parameters_comboBox.Enabled = False
        self.shared_parameters_comboBox.DropDownHeight = 150
        self.shared_parameters_comboBox.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.shared_parameters_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.shared_parameters_comboBox.FormattingEnabled = True
        self.shared_parameters_comboBox.IntegralHeight = True
        self.shared_parameters_comboBox.ItemHeight = 16
        self.shared_parameters_comboBox.Items.Insert(0, "Please select a Shared Parameter group...")
        self.shared_parameters_comboBox.SelectedIndex = 0
        self.shared_parameters_comboBox.Location = System.Drawing.Point(292, 5)
        self.shared_parameters_comboBox.MaxDropDownItems = 10
        self.shared_parameters_comboBox.Name = "shared_parameters_comboBox"
        self.shared_parameters_comboBox.Size = System.Drawing.Size(279, 24)
        self.shared_parameters_comboBox.TabIndex = 11
        self.shared_parameters_comboBox.SelectedValueChanged += self.shared_parameters_comboBox_SelValChanged
        # 
        # space_id_par_label
        # 
        self.space_id_par_label.Dock = WinForms.DockStyle.Fill
        self.space_id_par_label.AutoSize = True
        self.space_id_par_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.space_id_par_label.Location = System.Drawing.Point(5, 37)
        self.space_id_par_label.Margin = WinForms.Padding(0)
        self.tableLayoutPanel.SetRowSpan(self.space_id_par_label, 2)
        self.space_id_par_label.Name = "space_id_par_label"
        self.space_id_par_label.Size = System.Drawing.Size(279, 51)
        self.space_id_par_label.TabIndex = 0
        self.space_id_par_label.Text = "Space Identification Parameter"
        self.space_id_par_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        # 
        # pressure_cls_par_label
        # 
        self.pressure_cls_par_label.Dock = WinForms.DockStyle.Fill
        self.pressure_cls_par_label.AutoSize = True
        self.pressure_cls_par_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.pressure_cls_par_label.Location = System.Drawing.Point(5, 96)
        self.pressure_cls_par_label.Margin = WinForms.Padding(0)
        self.tableLayoutPanel.SetRowSpan(self.pressure_cls_par_label, 2)
        self.pressure_cls_par_label.Name = "pressure_cls_par_label"
        self.pressure_cls_par_label.Size = System.Drawing.Size(279, 51)
        self.pressure_cls_par_label.TabIndex = 1
        self.pressure_cls_par_label.Text = "Pressure Class Parameter"
        self.pressure_cls_par_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        # 
        # overflow_par_label
        # 
        self.overflow_par_label.Dock = WinForms.DockStyle.Fill
        self.overflow_par_label.AutoSize = True
        self.overflow_par_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.overflow_par_label.Location = System.Drawing.Point(5, 155)
        self.overflow_par_label.Margin = WinForms.Padding(0)
        self.tableLayoutPanel.SetRowSpan(self.overflow_par_label, 2)
        self.overflow_par_label.Name = "overflow_par_label"
        self.overflow_par_label.Size = System.Drawing.Size(279, 51)
        self.overflow_par_label.TabIndex = 2
        self.overflow_par_label.Text = "Overflow Air Parameter"
        self.overflow_par_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        # 
        # inflow_par_label
        # 
        self.inflow_par_label.Dock = WinForms.DockStyle.Fill
        self.inflow_par_label.AutoSize = True
        self.inflow_par_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.inflow_par_label.Location = System.Drawing.Point(5, 214)
        self.inflow_par_label.Margin = WinForms.Padding(0)
        self.tableLayoutPanel.SetRowSpan(self.inflow_par_label, 2)
        self.inflow_par_label.Name = "inflow_par_label"
        self.inflow_par_label.Size = System.Drawing.Size(279, 51)
        self.inflow_par_label.TabIndex = 3
        self.inflow_par_label.Text = "Inflow Air Parameter"
        self.inflow_par_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        # 
        # launch_label
        # 
        self.launch_label.Anchor = WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
        self.launch_label.AutoSize = True
        self.launch_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.launch_label.Location = System.Drawing.Point(5, 308)
        self.launch_label.Margin = WinForms.Padding(0)
        self.launch_label.Name = "launch_label"
        self.launch_label.Size = System.Drawing.Size(279, 20)
        self.launch_label.TabIndex = 4
        self.launch_label.Text = "Launch"
        self.launch_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        # 
        # space_id_par_comboBox
        # 
        self.space_id_par_comboBox.Anchor = WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
        self.space_id_par_comboBox.DropDownHeight = 150
        self.space_id_par_comboBox.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.space_id_par_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.space_id_par_comboBox.FormattingEnabled = True
        self.space_id_par_comboBox.IntegralHeight = False
        self.space_id_par_comboBox.ItemHeight = 16
        self.space_id_par_comboBox.Location = System.Drawing.Point(292, 37)
        self.space_id_par_comboBox.MaxDropDownItems = 10
        self.space_id_par_comboBox.Name = "space_id_par_comboBox"
        self.space_id_par_comboBox.Size = System.Drawing.Size(279, 24)
        self.space_id_par_comboBox.TabIndex = 5
        self.space_id_par_comboBox.SelectedValueChanged += self.space_id_par_comboBox_SelValChanged
        # 
        # pressure_cls_par_comboBox
        # 
        self.pressure_cls_par_comboBox.Anchor = WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
        self.pressure_cls_par_comboBox.DropDownHeight = 150
        self.pressure_cls_par_comboBox.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.pressure_cls_par_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.pressure_cls_par_comboBox.FormattingEnabled = True
        self.pressure_cls_par_comboBox.IntegralHeight = False
        self.pressure_cls_par_comboBox.ItemHeight = 16
        self.pressure_cls_par_comboBox.Location = System.Drawing.Point(292, 96)
        self.pressure_cls_par_comboBox.MaxDropDownItems = 10
        self.pressure_cls_par_comboBox.Name = "pressure_cls_par_comboBox"
        self.pressure_cls_par_comboBox.Size = System.Drawing.Size(279, 24)
        self.pressure_cls_par_comboBox.TabIndex = 6
        self.pressure_cls_par_comboBox.SelectedValueChanged += self.pressure_cls_par_comboBox_SelValChanged
        # 
        # overflow_par_comboBox
        # 
        self.overflow_par_comboBox.Anchor = WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
        self.overflow_par_comboBox.DropDownHeight = 150
        self.overflow_par_comboBox.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.overflow_par_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.overflow_par_comboBox.FormattingEnabled = True
        self.overflow_par_comboBox.IntegralHeight = False
        self.overflow_par_comboBox.ItemHeight = 16
        self.overflow_par_comboBox.Location = System.Drawing.Point(292, 155)
        self.overflow_par_comboBox.MaxDropDownItems = 10
        self.overflow_par_comboBox.Name = "overflow_par_comboBox"
        self.overflow_par_comboBox.Size = System.Drawing.Size(279, 24)
        self.overflow_par_comboBox.TabIndex = 7
        self.overflow_par_comboBox.SelectedValueChanged += self.overflow_par_comboBox_SelValChanged
        # 
        # inflow_par_comboBox
        # 
        self.inflow_par_comboBox.Anchor = WinForms.AnchorStyles.Left | WinForms.AnchorStyles.Right
        self.inflow_par_comboBox.DropDownHeight = 150
        self.inflow_par_comboBox.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.inflow_par_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
        self.inflow_par_comboBox.FormattingEnabled = True
        self.inflow_par_comboBox.IntegralHeight = False
        self.inflow_par_comboBox.ItemHeight = 16
        self.inflow_par_comboBox.Location = System.Drawing.Point(292, 214)
        self.inflow_par_comboBox.MaxDropDownItems = 10
        self.inflow_par_comboBox.Name = "inflow_par_comboBox"
        self.inflow_par_comboBox.Size = System.Drawing.Size(279, 24)
        self.inflow_par_comboBox.TabIndex = 8
        self.inflow_par_comboBox.SelectedValueChanged += self.inflow_par_comboBox_SelValChanged
        # 
        # run_button
        # 
        self.run_button.Anchor = WinForms.AnchorStyles.Bottom | WinForms.AnchorStyles.Right
        self.run_button.FlatAppearance.BorderColor = System.Drawing.Color.White
        self.run_button.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Gray
        self.run_button.Font = System.Drawing.Font("Microsoft Sans Serif", 14.25, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 204)
        self.run_button.Location = System.Drawing.Point(421, 325)
        self.run_button.Name = "run_button"
        self.run_button.Size = System.Drawing.Size(150, 39)
        self.run_button.TabIndex = 9
        self.run_button.Text = "RUN"
        self.run_button.UseVisualStyleBackColor = True
        self.run_button.Click += self.run_button_Clicked
        # 
        # space_id_par_textBox
        # 
        self.space_id_par_textBox.Dock = System.Windows.Forms.DockStyle.Fill
        self.space_id_par_textBox.Cursor = System.Windows.Forms.Cursors.No
        self.space_id_par_textBox.Location = System.Drawing.Point(292, 69)
        self.space_id_par_textBox.Name = "Space Identification Parameter"
        self.space_id_par_textBox.Size = System.Drawing.Size(279, 20)
        self.space_id_par_textBox.TabIndex = 12
        self.space_id_par_textBox.ReadOnly = True
        # 
        # pressure_cls_par_textBox
        # 
        self.pressure_cls_par_textBox.Dock = System.Windows.Forms.DockStyle.Fill
        self.pressure_cls_par_textBox.Cursor = System.Windows.Forms.Cursors.No
        self.pressure_cls_par_textBox.Location = System.Drawing.Point(292, 128)
        self.pressure_cls_par_textBox.Name = "Pressure Class Parameter"
        self.pressure_cls_par_textBox.Size = System.Drawing.Size(279, 20)
        self.pressure_cls_par_textBox.TabIndex = 13
        self.pressure_cls_par_textBox.ReadOnly = True
        # 
        # overflow_par_textBox
        # 
        self.overflow_par_textBox.Dock = System.Windows.Forms.DockStyle.Fill
        self.overflow_par_textBox.Cursor = System.Windows.Forms.Cursors.No
        self.overflow_par_textBox.Location = System.Drawing.Point(292, 187)
        self.overflow_par_textBox.Name = "Overflow Parameter"
        self.overflow_par_textBox.Size = System.Drawing.Size(279, 20)
        self.overflow_par_textBox.TabIndex = 14
        self.overflow_par_textBox.ReadOnly = True
        # 
        # inflow_par_textBox
        # 
        self.inflow_par_textBox.Dock = System.Windows.Forms.DockStyle.Fill
        self.inflow_par_textBox.Cursor = System.Windows.Forms.Cursors.No
        self.inflow_par_textBox.Location = System.Drawing.Point(292, 246)
        self.inflow_par_textBox.Name = "Inflow Parameter"
        self.inflow_par_textBox.Size = System.Drawing.Size(279, 20)
        self.inflow_par_textBox.TabIndex = 15
        self.inflow_par_textBox.ReadOnly = True
        # 
        # progressBar
        # 
        self.progressBar.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self.progressBar.Location = System.Drawing.Point(12, 526)
        self.progressBar.Name = "progressBar"
        self.progressBar.Size = System.Drawing.Size(576, 23)
        self.progressBar.Value = 0
        self.progressBar.TabIndex = 3
        # 
        # MainForm
        # 
        self.ClientSize = System.Drawing.Size(600, 600)
        self.Controls.Add(self.pars_set_groupBox)
        self.Controls.Add(self.door_pars_groupBox)
        self.Controls.Add(self.tableLayoutPanel)
        self.Controls.Add(self.progressBar)
        self.MinimumSize = System.Drawing.Size(600, 600)
        self.StartPosition = WinForms.FormStartPosition.CenterScreen
        self.Name = "MainForm"
        self.Text = "Calculate Room Overflows"
        self.tableLayoutPanel.ResumeLayout(False)
        self.tableLayoutPanel.PerformLayout()
        self.pars_set_groupBox.ResumeLayout(False)
        self.pars_set_groupBox.PerformLayout()
        self.door_pars_groupBox.ResumeLayout(False)
        self.door_pars_groupBox.PerformLayout()
        self.ResumeLayout(False)

    def dispose(self):
        self.components.Dispose()
        WinForms.Form.Dispose(self)
    
    def prj_pars_radio_button_CheckChng(self, sender, args):
        if sender.Checked:
            self.load_project_parameters()
            self.shared_parameters_comboBox.Enabled = False
            self.space_id_par_comboBox.Enabled = True
            self.pressure_cls_par_comboBox.Enabled = True
            self.overflow_par_comboBox.Enabled = True
            self.inflow_par_comboBox.Enabled = True
    
    def shr_pars_radio_button_CheckChng(self, sender, args):
        if sender.Checked:
            self.load_shared_par_groups()
            self.shared_parameters_comboBox.Enabled = True
            self.space_id_par_comboBox.Enabled = False
            self.pressure_cls_par_comboBox.Enabled = False
            self.overflow_par_comboBox.Enabled = False
            self.inflow_par_comboBox.Enabled = False

    def On_MainForm_Closing(self, sender, args):
        message = "Are you sure that you would like to close the form?"
        caption = "Form Closing"
        result = WinForms.MessageBox.Show(
            message, caption, WinForms.MessageBoxButtons.YesNo, WinForms.MessageBoxIcon.Question)

        # If the no button was pressed ...
        if result == WinForms.DialogResult.No:
            # cancel the closure of the form.
            args.Cancel = True

    def On_MainForm_StartUp(self, sender, args):
        self.load_project_parameters()

    def get_parameter_bindings(self):
        prj_defs_dict = {}
        binding_map = self.doc.ParameterBindings
        it = binding_map.ForwardIterator()
        it.Reset()
        while it.MoveNext():
            current_binding = it.Current
            if current_binding.Categories.Contains(Category.GetCategory(self.doc, BuiltInCategory.OST_MEPSpaces)):
                prj_defs_dict[it.Key.Name] = it.Key

        return prj_defs_dict

    def load_project_parameters(self):
        internal_defs = self.get_parameter_bindings()
        self.parameters = self.merge_two_dicts(self.parameters, internal_defs)
        for control in self.tableLayoutPanel.Controls:
                if control in (self.space_id_par_comboBox, self.pressure_cls_par_comboBox, 
                            self.overflow_par_comboBox, self.inflow_par_comboBox):
                    control.Enabled = True
                    control.Items.Clear()
                    control.BeginUpdate()
                    for par_name in sorted(internal_defs):
                        control.Items.Add(par_name)
                    control.EndUpdate()
                    control.Items.Insert(0, "Please select a parameter...")
                    control.SelectedIndex = 0
    
    def load_shared_par_groups(self):
        shr_par_file = self.app.OpenSharedParameterFile()
        self.par_groups = shr_par_file.Groups
        groups_list = sorted([group.Name for group in self.par_groups.GetEnumerator()])
        self.shared_parameters_comboBox.Items.Clear()
        self.shared_parameters_comboBox.BeginUpdate()
        for group in groups_list:
            self.shared_parameters_comboBox.Items.Add(group)
        self.shared_parameters_comboBox.EndUpdate()
        self.shared_parameters_comboBox.Items.Insert(0, "Please select a Shared Parameter group...")
        self.shared_parameters_comboBox.SelectedIndex = 0
    
    def get_ext_defs(self):
        self.par_group = self.par_groups.get_Item(self.shared_parameters_comboBox.SelectedItem)
        ext_defs_dict = {par.Name: par.GUID for par in self.par_group.Definitions}
        return ext_defs_dict

    def shared_parameters_comboBox_SelValChanged(self, sender, args):
        if self.shared_parameters_comboBox.SelectedIndex != 0:
            ext_defs = self.get_ext_defs()
            self.parameters = self.merge_two_dicts(self.parameters, ext_defs)
            for control in self.tableLayoutPanel.Controls:
                    if control in (self.space_id_par_comboBox, self.pressure_cls_par_comboBox, 
                                self.overflow_par_comboBox, self.inflow_par_comboBox):
                        control.Enabled = True
                        control.Items.Clear()
                        control.BeginUpdate()
                        for par_name in sorted(ext_defs):
                            control.Items.Add(par_name)
                        control.EndUpdate()
                        control.Items.Insert(0, "Please select a parameter...")
                        control.SelectedIndex = 0
        else:
            for control in self.tableLayoutPanel.Controls:
                if control in (self.space_id_par_comboBox, self.pressure_cls_par_comboBox, 
                                self.overflow_par_comboBox, self.inflow_par_comboBox):
                    control.Items.Clear()
                    control.Items.Insert(0, "Please select a parameter...")
                    control.SelectedIndex = 0
    
    def space_id_par_comboBox_SelValChanged(self, sender, args):
        if self.space_id_par_comboBox.SelectedIndex != 0: 
            self.space_id_par_textBox.Text = self.space_id_par_comboBox.SelectedItem
    
    def pressure_cls_par_comboBox_SelValChanged(self, sender, args):
        if self.pressure_cls_par_comboBox.SelectedIndex != 0:
            self.pressure_cls_par_textBox.Text = self.pressure_cls_par_comboBox.SelectedItem
    
    def overflow_par_comboBox_SelValChanged(self, sender, args):
        if self.overflow_par_comboBox.SelectedIndex != 0:
            self.overflow_par_textBox.Text = self.overflow_par_comboBox.SelectedItem
    
    def inflow_par_comboBox_SelValChanged(self, sender, args):
        if self.inflow_par_comboBox.SelectedIndex != 0:
            self.inflow_par_textBox.Text = self.inflow_par_comboBox.SelectedItem

    def run_button_Clicked(self, sender, args):

        unfilled_fields = filter(lambda x: x is not None, map(self.check_for_empty, (self.space_id_par_textBox, 
        self.pressure_cls_par_textBox, self.overflow_par_textBox, self.inflow_par_textBox)))
        
        if len(unfilled_fields) > 0:
            message = ", ".join(unfilled_fields) + ' unfilled!'
            WinForms.MessageBox.Show(message, "Error!", WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Exclamation)
            return

        space_id_par = self.parameters[self.space_id_par_textBox.Text]
        pressure_cls_par = self.parameters[self.pressure_cls_par_textBox.Text]
        overflow_par = self.parameters[self.overflow_par_textBox.Text]
        inflow_par = self.parameters[self.inflow_par_textBox.Text]

        self.calculation = CalculateRoomOverflows(self.doc, space_id_par, pressure_cls_par, overflow_par, inflow_par, 
        float(self.door_crack_width_textBox.Text), float(self.flow_coeff_textBox.Text))

        self.calculation.CalcStart += self.startProgressBar
        self.calculation.ReportProgress += self.updateProgressBar
        self.calculation.CalcEnd += self.disableProgressBar

        self.calculation.main()

    def startProgressBar(self, *args):
        self.progressBar.Maximum = args[0]

    def updateProgressBar(self, *args):
        self.progressBar.Value = args[0]

    def disableProgressBar(self, *args):
        if self.progressBar.Maximum > self.progressBar.Value:
            self.progressBar.Value = self.progressBar.Maximum
            WinForms.MessageBox.Show("Task completed successfully!", "Success!", 
            WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Information)
        
    def check_for_empty(self, control):
        if control.Text == "":
            return control.Name

    def merge_two_dicts(self, d1, d2):
        '''
        Merges two dictionaries
        Returns a merged dictionary
        '''
        d_merged = d1.copy()
        d_merged.update(d2)
        return d_merged

    def run(self):
        '''
        Start our form object
        '''
        # Run the Application
        WinForms.Application.Run(self)


class Event(object):
    def __init__(self):
        self.handlers = []

    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.handlers.remove(handler)
        return self

    def emit(self, *args):
        for handler in self.handlers:
            handler(*args)
