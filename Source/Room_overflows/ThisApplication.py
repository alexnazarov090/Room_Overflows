#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clr
clr.AddReference("RevitAPI.dll")
clr.AddReference("RevitAPIUI.dll")
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

import System.Windows.Forms as WinForms

from Autodesk.Revit import Attributes
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.UI.Macros import ApplicationEntryPoint
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import Category, FilteredElementCollector, TransactionGroup, Transaction, TransactionStatus
from Autodesk.Revit.DB import UnitUtils, DisplayUnitType, BuiltInParameter, BuiltInCategory, ElementId, XYZ
from Autodesk.Revit.DB import ParameterValueProvider, FilterStringContains, FilterStringRule, ElementParameterFilter
from Autodesk.Revit.DB import FamilySymbol, FamilyInstanceFilter, Line, ElementTransformUtils, View, ViewDiscipline, ViewType
from Autodesk.Revit.DB.Structure import StructuralType

import sys
path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(path)
import os
sys.path.append(os.path.realpath(__file__))
from MainForm import MainForm
import math
import re
import logging
import json
import io
from collections import namedtuple, OrderedDict

# Logger
dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.DEBUG,
                    filename=r'{}'.format(os.path.join(dir_path, 'ThisApplication.log')),
                    filemode='w',
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


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
        view = MainForm()
        model = CalculateRoomOverflows(self)     
        controller = Controller(self, view=view, model=model)
    
        controller.run()


class CalculateRoomOverflows(object):
    def __init__(self, __revit__, space_id_par=None,  pressure_cls_par=None, 
                overflow_par=None, inflow_par=None, 
                door_crack_width=0.001, flow_coefficient=0.7):
                
        self.doc = __revit__.ActiveUIDocument.Document
        self.uidoc = UIDocument(self.doc)
        self._space_id_par = space_id_par
        self._pressure_cls_par = pressure_cls_par
        self._overflow_par = overflow_par
        self._inflow_par = inflow_par
        self._door_crack_width = door_crack_width
        self._flow_coefficient = flow_coefficient

        self.CalcStart = Event()
        self.ReportProgress = Event()
        self.CalcEnd = Event()

    # region Getters and Setters
    @property
    def space_id_par(self):
        return self._space_id_par

    @space_id_par.setter
    def space_id_par(self, value):
        self._space_id_par = value
    
    @property
    def pressure_cls_par(self):
        return self._pressure_cls_par

    @pressure_cls_par.setter
    def pressure_cls_par(self, value):
        self._pressure_cls_par = value
    
    @property
    def overflow_par(self):
        return self._overflow_par

    @overflow_par.setter
    def overflow_par(self, value):
        self._overflow_par = value
    
    @property
    def inflow_par(self):
        return self._inflow_par

    @inflow_par.setter
    def inflow_par(self, value):
        self._inflow_par = value
    
    @property
    def door_crack_width(self):
        return self._door_crack_width

    @door_crack_width.setter
    def door_crack_width(self, value):
        self._door_crack_width = value
    
    @property
    def flow_coefficient(self):
        return self._flow_coefficient

    @flow_coefficient.setter
    def flow_coefficient(self, value):
        self._flow_coefficient = value
    # endregion Getters and Setters

    def main(self):
        try:
            sel = self.uidoc.Selection
            ref = sel.PickObject(ObjectType.Element, "Please pick a linked model instance")
            rvt_link = self.doc.GetElement(ref.ElementId)
            self.linkedDoc = rvt_link.GetLinkDocument()
            self.transform = rvt_link.GetTotalTransform()

            self.doors = FilteredElementCollector(self.linkedDoc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_Doors).ToElements()
            self.spaces = FilteredElementCollector(self.doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_MEPSpaces).ToElements()
            self.views_dict = self.get_mech_views()
            self.arrow_families = self.get_arrow_families()

            progress_bar_length = len(self.doors) + 3*(len(self.spaces)) + len(self.arrow_families)
            self.counter = 0

            self.CalcStart.emit(progress_bar_length)
            self.__main()
            self.CalcEnd.emit()

            
            
        except Exception as e:
            logger.error(e, exc_info=True)
            WinForms.MessageBox.Show("Error in obtaining linked model", "Error!", WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Error)
            return

    def __main(self):
        with TransactionGroup(self.doc, 'Calculate Room Overflows') as tg:
            tg.Start()

            try:
                self.spaces_data = {space.get_Parameter(self._space_id_par).AsString(): space for space in self.spaces}
            
            except Exception as e:
                logger.error(e, exc_info=True)
                WinForms.MessageBox.Show("Task failed!", "Error!", WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Error)
                return

            with Transaction(self.doc, 'Reset overflow/inflow values') as tr:
                tr.Start()
                self.reset_overflows(self.spaces)
                tr.Commit()
            
            if len(self.arrow_families) > 0:
                with Transaction(self.doc, 'Delete arrows') as tr:
                    tr.Start()
                    self.delete_arrows(self.arrow_families)
                    tr.Commit()

            overflows_data = {}
            inflows_data = {}
            phases = self.linkedDoc.Phases
            phase = phases[phases.Size - 1]

            for door in self.doors:
                try:
                    room1 = door.FromRoom[phase]
                    room2 = door.ToRoom[phase]
                    if room1 and room2:
                        airflow, overflow_space, inflow_space = self.calculate_overflow(door, (room1, room2))
                        overflows_data[overflow_space] = overflows_data.get(overflow_space, 0) + airflow
                        inflows_data[inflow_space] = inflows_data.get(inflow_space, 0) + airflow

                        if airflow > 0:
                            self.insert_arrow(door, overflow_space, inflow_space, airflow)

                except Exception as e:
                    logger.error(e, exc_info=True)
                    pass

                self.counter += 1
                self.ReportProgress.emit(self.counter)

            with Transaction(self.doc, "Set overflows") as tr:
                tr.Start()
                try:
                    for overflow_space, overflow in overflows_data.items():
                    
                        room_overflow_par = overflow_space.get_Parameter(self._overflow_par)
                        conv_val = UnitUtils.ConvertToInternalUnits(overflow, DisplayUnitType.DUT_CUBIC_METERS_PER_HOUR)
                        room_overflow_par.Set(conv_val)
                        self.counter += 1
                        self.ReportProgress.emit(self.counter)

                    for inflow_space, inflow in inflows_data.items():
                    
                        room_inflow_par = inflow_space.get_Parameter(self._inflow_par)
                        conv_val = UnitUtils.ConvertToInternalUnits(inflow, DisplayUnitType.DUT_CUBIC_METERS_PER_HOUR)
                        room_inflow_par.Set(conv_val)
                        self.counter += 1
                        self.ReportProgress.emit(self.counter)

                except Exception as e:
                    logger.error(e, exc_info=True)
                    pass
                tr.Commit()

            commit_status = tg.Assimilate()

            if commit_status != TransactionStatus.Committed: 
                WinForms.MessageBox.Show("Task failed!", "Error!", 
                WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Error)
                return
    
    def calculate_overflow(self, door, rooms):
        door_width = float(door.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsValueString())
        door_height = float(door.get_Parameter(BuiltInParameter.DOOR_HEIGHT).AsValueString())
        
        if door_width == 0 and door_height == 0:
            door_width = float(door.Symbol.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsValueString())
            door_height = float(door.Symbol.get_Parameter(BuiltInParameter.DOOR_HEIGHT).AsValueString())

        if door_width < 1300:
            door_crack_area = (2*(door_width/1000 + door_height/1000))*self._door_crack_width
        else:
            door_crack_area = (2*(door_width/1000 + door_height/1000) + door_height/1000)*self._door_crack_width
        
        mu = float(self._flow_coefficient)
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
        
        SpacesData = namedtuple('SpacesData', ['space_id', 'pressure'])

        sorted_spaces = sorted(room_pressures.items(), key=lambda x: x[1], reverse=True)
        overflow_space = SpacesData(*sorted_spaces[0])
        inflow_space = SpacesData(*sorted_spaces[1])

        P1 = overflow_space.pressure
        P2 = inflow_space.pressure
        dP = P1 - P2
        
        dL = 3600*door_crack_area*mu*math.sqrt((2*dP)/1.2)
        
        return dL, overflow_space.space_id, inflow_space.space_id

    def reset_overflows(self, spaces):
        try:
            for space in spaces:
            
                overflow_par = space.get_Parameter(self._overflow_par)
                overflow_par.Set(0)
        except Exception as e:
                logger.error(e, exc_info=True)
                pass
            
        try:
                inflow_par = space.get_Parameter(self._inflow_par)
                inflow_par.Set(0)
        except Exception as e:
                logger.error(e, exc_info=True)
                pass

        self.counter += 1
        self.ReportProgress.emit(self.counter)

    def get_arrow_families(self):
        try:
            arrow_family_id = self.get_arrow_family_type().Id
            param_filter = FamilyInstanceFilter(self.doc, arrow_family_id)
            arrow_family_instances = FilteredElementCollector(self.doc).WherePasses(param_filter).ToElements()

            return arrow_family_instances

        except Exception as e:
                logger.error(e, exc_info=True)
                pass

    def delete_arrows(self, arrows):
        try:
            for arrow in arrows:
                self.doc.Delete(arrow.Id)
                

        except Exception as e:
                logger.error(e, exc_info=True)
                pass

        self.counter += 1
        self.ReportProgress.emit(self.counter)

    def get_mech_views(self):

        try:
            views = FilteredElementCollector(self.doc).WhereElementIsNotElementType().OfClass(View)

            views_dict = {view.GenLevel.UniqueId: view for view in views
                        if view.Name and view.GenLevel
                        and view.ViewType == ViewType.FloorPlan
                        and view.Discipline == ViewDiscipline.Mechanical}

            return views_dict

        except Exception as e:
                logger.error(e, exc_info=True)
                pass

    def get_arrow_family_type(self):
        try:
            family_sym_name_param_prov = ParameterValueProvider(ElementId(BuiltInParameter.SYMBOL_NAME_PARAM))
            param_equality = FilterStringContains()
            family_sym_name_value_rule = FilterStringRule(family_sym_name_param_prov, 
                                                    param_equality, 
                                                    "Arrow Wide", 
                                                    False)
            param_filter = ElementParameterFilter(family_sym_name_value_rule)
            arrow_family_type = FilteredElementCollector(self.doc).OfClass(FamilySymbol).WherePasses(param_filter).FirstElement()
            return arrow_family_type

        except Exception as e:
                logger.error(e, exc_info=True)
                return

    def insert_arrow(self, door, overflow_space, inflow_space, airflow):
        try:
            with Transaction(self.doc, "Insert Arrow") as tr:
                tr.Start()
                arrow_symbol = self.get_arrow_family_type()
                if not arrow_symbol.IsActive:
                    arrow_symbol.Activate()
                    self.doc.Regenerate()

                current_level_id = overflow_space.Level.UniqueId

                door_coords = self.transform.OfPoint(door.Location.Point)
                arrow_instance = self.doc.Create.NewFamilyInstance(door_coords, arrow_symbol, self.views_dict.get(current_level_id))
                
                door_orientation = door.FacingOrientation

                point1 = door_coords
                point2 = door_coords + XYZ(0, 0, 10)
                axis = Line.CreateBound(point1, point2)
                angleToRotate = 0

                door_bbox = door.get_BoundingBox(self.views_dict.get(current_level_id))

                if int(door_orientation.X) in (-1, 1):

                    if overflow_space.IsPointInSpace(self.transform.OfPoint(door_bbox.Min)
                    ) or inflow_space.IsPointInSpace(self.transform.OfPoint(door_bbox.Max)):
                        angleToRotate = -90

                    elif overflow_space.IsPointInSpace(self.transform.OfPoint(door_bbox.Max)
                    ) or inflow_space.IsPointInSpace(self.transform.OfPoint(door_bbox.Min)):
                        angleToRotate = 90

                else:
                
                    if overflow_space.IsPointInSpace(self.transform.OfPoint(door_bbox.Max)
                    ) or inflow_space.IsPointInSpace(self.transform.OfPoint(door_bbox.Min)):
                        angleToRotate = 180

                ElementTransformUtils.RotateElement(self.doc, arrow_instance.Id, axis, ((math.pi / 180) * angleToRotate))
                
                tr.Commit()

        except Exception as e:
                logger.error(e, exc_info=True)
                pass

        try:
            with Transaction(self.doc, "Set Air Leakage") as tr:
                tr.Start()

                air_leakage_par = arrow_instance.GetParameters("Air Leakage")[0]
                conv_val = UnitUtils.ConvertToInternalUnits(airflow, DisplayUnitType.DUT_CUBIC_METERS_PER_HOUR)
                air_leakage_par.Set(conv_val)

                tr.Commit()

        except Exception as e:
                logger.error(e, exc_info=True)
                pass


class Controller(object):
    def __init__(self, __revit__, view, model):
        self.app = __revit__.Application
        self.doc = __revit__.ActiveUIDocument.Document
        self._view = view
        self._model = model
        self.parameters = {}
        self.config_file_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.open_config_file_Dialog = WinForms.OpenFileDialog()
        self.save_config_file_Dialog = WinForms.SaveFileDialog()

        self._connectSignals()

    def _connectSignals(self):
        self._view.Shown += self.On_MainForm_StartUp
        self._view.FormClosing += self.On_MainForm_Closing
        self._view._prj_pars_radio_button.CheckedChanged += self.prj_pars_radio_button_CheckChng
        self._view._shr_pars_radio_button.CheckedChanged += self.shr_pars_radio_button_CheckChng
        self._view._shared_parameters_comboBox.SelectedValueChanged += self.shared_parameters_comboBox_SelValChanged
        self._view._space_id_par_comboBox.SelectedValueChanged += self._space_id_par_comboBox_SelValChanged
        self._view._pressure_cls_par_comboBox.SelectedValueChanged += self.pressure_cls_par_comboBox_SelValChanged
        self._view._overflow_par_comboBox.SelectedValueChanged += self._overflow_par_comboBox_SelValChanged
        self._view._inflow_par_comboBox.SelectedValueChanged += self._inflow_par_comboBox_SelValChanged
        self._view._views_treeView.AfterCheck += self.node_AfterCheck
        self._view._run_button.Click += self.run_button_Clicked
        self._view._load_stngs_button.Click += lambda _, __: self.load_settings()
        self._view._save_stngs_button.Click += lambda _, __: self.save_settings()

        self._model.CalcStart += self.startProgressBar
        self._model.ReportProgress += self.updateProgressBar
        self._model.CalcEnd += self.disableProgressBar

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
        self.populate_views_tree()

    def save_settings(self):

        try:
            filename = self._view._config_file_path_textBox.Text

            if self._view._config_file_path_textBox.Text == "":

                self.save_config_file_Dialog.InitialDirectory = self.config_file_dir_path
                self.save_config_file_Dialog.Filter = "JSON files (*.json)|*.json|All files (*.*)|*.*"
                self.save_config_file_Dialog.FilterIndex = 1
                self.save_config_file_Dialog.RestoreDirectory = True

                result = self.save_config_file_Dialog.ShowDialog(self._view)
                if result == WinForms.DialogResult.OK:
                    filename = self.save_config_file_Dialog.FileName
                    self._view._config_file_path_textBox.Text = filename
                else:
                    return
                    
            config = {}
            for item in (self._view._door_pars_groupBox.Controls, self._view._tableLayoutPanel.Controls):
                    for c in item:
                        if c.GetType() == clr.GetClrType(WinForms.ComboBox):
                            config[c.Name] = c.SelectedItem
                        elif c.GetType() == clr.GetClrType(WinForms.TextBox):
                            config[c.Name] = c.Text
                        elif c.GetType() == clr.GetClrType(WinForms.CheckedListBox):
                            config[c.Name] = c.CheckedItems

            with io.open(filename,
                        'w', encoding='utf8') as file:
                json.dump(config, file, ensure_ascii=False, indent=4, sort_keys=True)

        except Exception as e:
            logger.error(e, exc_info=True)

    def load_settings(self):

        self.open_config_file_Dialog.InitialDirectory = self.config_file_dir_path
        self.open_config_file_Dialog.Filter = "JSON files (*.json)|*.json"
        self.open_config_file_Dialog.FilterIndex = 2
        self.open_config_file_Dialog.RestoreDirectory = True

        result = self.open_config_file_Dialog.ShowDialog(self._view)
        if result == WinForms.DialogResult.OK:
            self._view._config_file_path_textBox.Clear()
            filename = self.open_config_file_Dialog.FileName
            self._view._config_file_path_textBox.Text = filename
        else:
            return

        try:
            with io.open(filename,
                        'r', encoding='utf8') as file:
                config = json.load(file)
                for item in (self._view._door_pars_groupBox.Controls, self._view._tableLayoutPanel.Controls):
                    for c in item:
                        if c.GetType() == clr.GetClrType(WinForms.ComboBox):
                            c.SelectedItem = config[c.Name]
                        elif c.GetType() == clr.GetClrType(WinForms.TextBox):
                            c.Text = config[c.Name]
                        elif c.GetType() == clr.GetClrType(WinForms.CheckedListBox):
                            for item in config[c.Name]:
                                index = c.FindStringExact(item)
                                if (index != c.NoMatches):
                                    c.SetItemChecked(index, True)

        except Exception as e:
            logger.error(e, exc_info=True)

    def prj_pars_radio_button_CheckChng(self, sender, args):
        if sender.Checked:
            self.load_project_parameters()
            self._view._shared_parameters_comboBox.Enabled = False
            self._view._space_id_par_comboBox.Enabled = True
            self._view._pressure_cls_par_comboBox.Enabled = True
            self._view._overflow_par_comboBox.Enabled = True
            self._view._inflow_par_comboBox.Enabled = True
    
    def shr_pars_radio_button_CheckChng(self, sender, args):
        if sender.Checked:
            self.load_shared_par_groups()
            self._view._shared_parameters_comboBox.Enabled = True
            self._view._space_id_par_comboBox.Enabled = False
            self._view._pressure_cls_par_comboBox.Enabled = False
            self._view._overflow_par_comboBox.Enabled = False
            self._view._inflow_par_comboBox.Enabled = False

    def load_views(self):
        try:
            views_collector = FilteredElementCollector(self.doc).WhereElementIsNotElementType().OfClass(View)

            views_dict = {view.Name: view for view in views_collector
                        if view.Name and view.GenLevel
                        and view.ViewType == ViewType.FloorPlan
                        and (view.Discipline == ViewDiscipline.Mechanical
                        or view.Discipline == ViewDiscipline.Coordination)}

            return OrderedDict(sorted(views_dict.items()))

        except Exception as e:
                logger.error(e, exc_info=True)
                pass

    def populate_views_tree(self):
        try:
            views = self.load_views()
            self._view._views_treeView.BeginUpdate()
            self._view._views_treeView.Nodes[0].Nodes[0].Nodes.Clear()
            self._view._views_treeView.Nodes[1].Nodes[0].Nodes.Clear()

            for name, view in views.items():
                if view.Discipline == ViewDiscipline.Coordination:
                    self._view._views_treeView.Nodes[0].Nodes[0].Nodes.Add(name)

                elif view.Discipline == ViewDiscipline.Mechanical:
                    self._view._views_treeView.Nodes[1].Nodes[0].Nodes.Add(name)

            self._view._views_treeView.EndUpdate()
        
        except Exception as e:
                logger.error(e, exc_info=True)
                pass

    # Updates all child tree nodes recursively.
    def check_all_child_nodes(self, treeNode, nodeChecked):
        for node in treeNode.Nodes:
            node.Checked = nodeChecked
            if(node.Nodes.Count > 0):
                # If the current node has child nodes, call the CheckAllChildsNodes method recursively.
                self.check_all_child_nodes(node, nodeChecked)


    def node_AfterCheck(self, sender, args):
        # The code only executes if the user caused the checked state to change.
        if(args.Action != WinForms.TreeViewAction.Unknown):
            if(args.Node.Nodes.Count > 0):
                # Calls the CheckAllChildNodes method, passing in the current 
                # Checked value of the TreeNode whose checked state changed.
                self.check_all_child_nodes(args.Node, args.Node.Checked)


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
        for control in (self._view._space_id_par_comboBox, self._view._pressure_cls_par_comboBox, 
                        self._view._overflow_par_comboBox, self._view._inflow_par_comboBox):
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
        self._view._shared_parameters_comboBox.Items.Clear()
        self._view._shared_parameters_comboBox.BeginUpdate()
        for group in groups_list:
            self._view._shared_parameters_comboBox.Items.Add(group)
        self._view._shared_parameters_comboBox.EndUpdate()
        self._view._shared_parameters_comboBox.Items.Insert(0, "Please select a Shared Parameter group...")
        self._view._shared_parameters_comboBox.SelectedIndex = 0
    
    def get_ext_defs(self):
        self.par_group = self.par_groups.get_Item(self._view._shared_parameters_comboBox.SelectedItem)
        ext_defs_dict = {par.Name: par.GUID for par in self.par_group.Definitions}
        return ext_defs_dict

    def shared_parameters_comboBox_SelValChanged(self, sender, args):
        if self._view._shared_parameters_comboBox.SelectedIndex != 0:
            ext_defs = self.get_ext_defs()
            self.parameters = self.merge_two_dicts(self.parameters, ext_defs)
            for control in (self._view._space_id_par_comboBox, self._view._pressure_cls_par_comboBox, 
                            self._view._overflow_par_comboBox, self._view._inflow_par_comboBox):
                        control.Enabled = True
                        control.Items.Clear()
                        control.BeginUpdate()
                        for par_name in sorted(ext_defs):
                            control.Items.Add(par_name)
                        control.EndUpdate()
                        control.Items.Insert(0, "Please select a parameter...")
                        control.SelectedIndex = 0
        else:
            for control in (self._view._space_id_par_comboBox, self._view._pressure_cls_par_comboBox, 
                            self._view._overflow_par_comboBox, self._view._inflow_par_comboBox):
                    control.Items.Clear()
                    control.Items.Insert(0, "Please select a parameter...")
                    control.SelectedIndex = 0
    
    def _space_id_par_comboBox_SelValChanged(self, sender, args):
        if sender.SelectedIndex != 0: 
            self._view._space_id_par_textBox.Text = sender.SelectedItem
            
    def pressure_cls_par_comboBox_SelValChanged(self, sender, args):
        if sender.SelectedIndex != 0:
            self._view._pressure_cls_par_textBox.Text = sender.SelectedItem
    
    def _overflow_par_comboBox_SelValChanged(self, sender, args):
        if sender.SelectedIndex != 0:
            self._view._overflow_par_textBox.Text = sender.SelectedItem
    
    def _inflow_par_comboBox_SelValChanged(self, sender, args):
        if sender.SelectedIndex != 0:
            self._view._inflow_par_textBox.Text = sender.SelectedItem

    def run_button_Clicked(self, sender, args):

        unfilled_fields = filter(lambda x: x is not None, map(self.check_for_empty, 
        (self._view._space_id_par_textBox, 
        self._view._pressure_cls_par_textBox, 
        self._view._overflow_par_textBox, 
        self._view._inflow_par_textBox, 
        self._view._door_crack_width_textBox, 
        self._view._flow_coeff_textBox)))
        
        if len(unfilled_fields) > 0:
            message = ", ".join(unfilled_fields) + ' unfilled!'
            WinForms.MessageBox.Show(message, "Error!", WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Exclamation)
            return

        self._model.space_id_par = self.parameters[self._view._space_id_par_textBox.Text]
        self._model.pressure_cls_par = self.parameters[self._view._pressure_cls_par_textBox.Text]
        self._model.overflow_par = self.parameters[self._view._overflow_par_textBox.Text]
        self._model.inflow_par = self.parameters[self._view._inflow_par_textBox.Text]
        self._model.door_crack_width = float(self._view._door_crack_width_textBox.Text)
        self._model.flow_coefficient = float(self._view._flow_coeff_textBox.Text)

        self._model.main()

    def startProgressBar(self, *args):
        self._view._progressBar.Maximum = args[0]

    def updateProgressBar(self, *args):
        self._view._progressBar.Value = args[0]

    def disableProgressBar(self, *args):
        if self._view._progressBar.Maximum > self._view._progressBar.Value:
            self._view._progressBar.Value = self._view._progressBar.Maximum
            WinForms.MessageBox.Show("Task completed successfully!", "Success!", 
            WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Information)
        
    def check_for_empty(self, control):
        if control.Text == "":
            return control.Tag

    def merge_two_dicts(self, d1, d2):
        '''
        Merges two dictionaries
        Returns a merged dictionary
        '''
        d_merged = d1.copy()
        d_merged.update(d2)
        return d_merged

    def dispose(self):
        self._view.components.Dispose()
        WinForms.Form.Dispose(self._view)

    def run(self):
        '''
        Start our form object
        '''
        # Run the Application
        WinForms.Application.Run(self._view)


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

