import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

class MainForm(Form):
	def __init__(self):
		self.InitializeComponent()
	
	def InitializeComponent(self):
		self._tableLayoutPanel = System.Windows.Forms.TableLayoutPanel()
		self._space_id_par_label = System.Windows.Forms.Label()
		self._pressure_cls_par_label = System.Windows.Forms.Label()
		self._overflow_par_label = System.Windows.Forms.Label()
		self._inflow_par_label = System.Windows.Forms.Label()
		self._launch_label = System.Windows.Forms.Label()
		self._space_id_par_comboBox = System.Windows.Forms.ComboBox()
		self._pressure_cls_par_comboBox = System.Windows.Forms.ComboBox()
		self._overflow_par_comboBox = System.Windows.Forms.ComboBox()
		self._inflow_par_comboBox = System.Windows.Forms.ComboBox()
		self._run_button = System.Windows.Forms.Button()
		self._pars_set_groupBox = System.Windows.Forms.GroupBox()
		self._prj_pars_radio_button = System.Windows.Forms.RadioButton()
		self._shr_pars_radio_button = System.Windows.Forms.RadioButton()
		self._shared_parameters_label = System.Windows.Forms.Label()
		self._shared_parameters_comboBox = System.Windows.Forms.ComboBox()
		self._space_id_par_textBox = System.Windows.Forms.TextBox()
		self._pressure_cls_par_textBox = System.Windows.Forms.TextBox()
		self._overflow_par_textBox = System.Windows.Forms.TextBox()
		self._inflow_par_textBox = System.Windows.Forms.TextBox()
		self._door_pars_groupBox = System.Windows.Forms.GroupBox()
		self._door_crack_width_label = System.Windows.Forms.Label()
		self._door_crack_width_textBox = System.Windows.Forms.TextBox()
		self._flow_coeff_label = System.Windows.Forms.Label()
		self._flow_coeff_textBox = System.Windows.Forms.TextBox()
		self._progressBar = System.Windows.Forms.ProgressBar()
		self._settings_groupBox = System.Windows.Forms.GroupBox()
		self._config_file_path_label = System.Windows.Forms.Label()
		self._config_file_path_textBox = System.Windows.Forms.TextBox()
		self._load_stngs_button = System.Windows.Forms.Button()
		self._save_stngs_button = System.Windows.Forms.Button()
		self._tableLayoutPanel.SuspendLayout()
		self._pars_set_groupBox.SuspendLayout()
		self._door_pars_groupBox.SuspendLayout()
		self._settings_groupBox.SuspendLayout()
		self.SuspendLayout()
		# 
		# tableLayoutPanel
		# 
		self._tableLayoutPanel.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._tableLayoutPanel.BackColor = System.Drawing.SystemColors.Control
		self._tableLayoutPanel.CellBorderStyle = System.Windows.Forms.TableLayoutPanelCellBorderStyle.Single
		self._tableLayoutPanel.ColumnCount = 2
		self._tableLayoutPanel.ColumnStyles.Add(System.Windows.Forms.ColumnStyle())
		self._tableLayoutPanel.ColumnStyles.Add(System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100))
		self._tableLayoutPanel.Controls.Add(self._pressure_cls_par_label, 0, 3)
		self._tableLayoutPanel.Controls.Add(self._overflow_par_label, 0, 5)
		self._tableLayoutPanel.Controls.Add(self._inflow_par_label, 0, 7)
		self._tableLayoutPanel.Controls.Add(self._launch_label, 0, 9)
		self._tableLayoutPanel.Controls.Add(self._space_id_par_comboBox, 1, 1)
		self._tableLayoutPanel.Controls.Add(self._pressure_cls_par_comboBox, 1, 3)
		self._tableLayoutPanel.Controls.Add(self._overflow_par_comboBox, 1, 5)
		self._tableLayoutPanel.Controls.Add(self._inflow_par_comboBox, 1, 7)
		self._tableLayoutPanel.Controls.Add(self._run_button, 1, 9)
		self._tableLayoutPanel.Controls.Add(self._shared_parameters_label, 0, 0)
		self._tableLayoutPanel.Controls.Add(self._space_id_par_label, 0, 1)
		self._tableLayoutPanel.Controls.Add(self._shared_parameters_comboBox, 1, 0)
		self._tableLayoutPanel.Controls.Add(self._space_id_par_textBox, 1, 2)
		self._tableLayoutPanel.Controls.Add(self._pressure_cls_par_textBox, 1, 4)
		self._tableLayoutPanel.Controls.Add(self._overflow_par_textBox, 1, 6)
		self._tableLayoutPanel.Controls.Add(self._inflow_par_textBox, 1, 8)
		self._tableLayoutPanel.Location = System.Drawing.Point(12, 141)
		self._tableLayoutPanel.Name = "tableLayoutPanel"
		self._tableLayoutPanel.RowCount = 10
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10))
		self._tableLayoutPanel.Size = System.Drawing.Size(560, 369)
		self._tableLayoutPanel.TabIndex = 2
		# 
		# space_id_par_label
		# 
		self._space_id_par_label.AutoSize = True
		self._space_id_par_label.Dock = System.Windows.Forms.DockStyle.Fill
		self._space_id_par_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._space_id_par_label.Location = System.Drawing.Point(1, 37)
		self._space_id_par_label.Margin = System.Windows.Forms.Padding(0)
		self._space_id_par_label.Name = "space_id_par_label"
		self._tableLayoutPanel.SetRowSpan(self._space_id_par_label, 2)
		self._space_id_par_label.Size = System.Drawing.Size(228, 71)
		self._space_id_par_label.TabIndex = 1
		self._space_id_par_label.Text = "Space Identification Parameter"
		self._space_id_par_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# pressure_cls_par_label
		# 
		self._pressure_cls_par_label.AutoSize = True
		self._pressure_cls_par_label.Dock = System.Windows.Forms.DockStyle.Fill
		self._pressure_cls_par_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._pressure_cls_par_label.Location = System.Drawing.Point(4, 112)
		self._pressure_cls_par_label.Margin = System.Windows.Forms.Padding(3)
		self._pressure_cls_par_label.Name = "pressure_cls_par_label"
		self._tableLayoutPanel.SetRowSpan(self._pressure_cls_par_label, 2)
		self._pressure_cls_par_label.Size = System.Drawing.Size(222, 65)
		self._pressure_cls_par_label.TabIndex = 2
		self._pressure_cls_par_label.Text = "Pressure Class Parameter"
		self._pressure_cls_par_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# overflow_par_label
		# 
		self._overflow_par_label.AutoSize = True
		self._overflow_par_label.Dock = System.Windows.Forms.DockStyle.Fill
		self._overflow_par_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._overflow_par_label.Location = System.Drawing.Point(4, 184)
		self._overflow_par_label.Margin = System.Windows.Forms.Padding(3)
		self._overflow_par_label.Name = "overflow_par_label"
		self._tableLayoutPanel.SetRowSpan(self._overflow_par_label, 2)
		self._overflow_par_label.Size = System.Drawing.Size(222, 65)
		self._overflow_par_label.TabIndex = 3
		self._overflow_par_label.Text = "Overflow Air Parameter"
		self._overflow_par_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# inflow_par_label
		# 
		self._inflow_par_label.AutoSize = True
		self._inflow_par_label.Dock = System.Windows.Forms.DockStyle.Fill
		self._inflow_par_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._inflow_par_label.Location = System.Drawing.Point(4, 256)
		self._inflow_par_label.Margin = System.Windows.Forms.Padding(3)
		self._inflow_par_label.Name = "inflow_par_label"
		self._tableLayoutPanel.SetRowSpan(self._inflow_par_label, 2)
		self._inflow_par_label.Size = System.Drawing.Size(222, 65)
		self._inflow_par_label.TabIndex = 4
		self._inflow_par_label.Text = "Inflow Air Parameter"
		self._inflow_par_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# launch_label
		# 
		self._launch_label.Anchor = System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._launch_label.AutoSize = True
		self._launch_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._launch_label.Location = System.Drawing.Point(4, 336)
		self._launch_label.Margin = System.Windows.Forms.Padding(3)
		self._launch_label.Name = "launch_label"
		self._launch_label.Size = System.Drawing.Size(222, 20)
		self._launch_label.TabIndex = 5
		self._launch_label.Text = "Launch"
		self._launch_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# space_id_par_comboBox
		# 
		self._space_id_par_comboBox.Anchor = System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._space_id_par_comboBox.DropDownHeight = 150
		self._space_id_par_comboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._space_id_par_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._space_id_par_comboBox.FormattingEnabled = True
		self._space_id_par_comboBox.IntegralHeight = False
		self._space_id_par_comboBox.ItemHeight = 16
		self._space_id_par_comboBox.Location = System.Drawing.Point(233, 42)
		self._space_id_par_comboBox.MaxDropDownItems = 10
		self._space_id_par_comboBox.Name = "space_id_par_comboBox"
		self._space_id_par_comboBox.Size = System.Drawing.Size(323, 24)
		self._space_id_par_comboBox.TabIndex = 7
		# 
		# pressure_cls_par_comboBox
		# 
		self._pressure_cls_par_comboBox.Anchor = System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._pressure_cls_par_comboBox.DropDownHeight = 150
		self._pressure_cls_par_comboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._pressure_cls_par_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._pressure_cls_par_comboBox.FormattingEnabled = True
		self._pressure_cls_par_comboBox.IntegralHeight = False
		self._pressure_cls_par_comboBox.ItemHeight = 16
		self._pressure_cls_par_comboBox.Location = System.Drawing.Point(233, 114)
		self._pressure_cls_par_comboBox.MaxDropDownItems = 10
		self._pressure_cls_par_comboBox.Name = "pressure_cls_par_comboBox"
		self._pressure_cls_par_comboBox.Size = System.Drawing.Size(323, 24)
		self._pressure_cls_par_comboBox.TabIndex = 9
		# 
		# overflow_par_comboBox
		# 
		self._overflow_par_comboBox.Anchor = System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._overflow_par_comboBox.DropDownHeight = 150
		self._overflow_par_comboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._overflow_par_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._overflow_par_comboBox.FormattingEnabled = True
		self._overflow_par_comboBox.IntegralHeight = False
		self._overflow_par_comboBox.ItemHeight = 16
		self._overflow_par_comboBox.Location = System.Drawing.Point(233, 186)
		self._overflow_par_comboBox.MaxDropDownItems = 10
		self._overflow_par_comboBox.Name = "overflow_par_comboBox"
		self._overflow_par_comboBox.Size = System.Drawing.Size(323, 24)
		self._overflow_par_comboBox.TabIndex = 11
		# 
		# inflow_par_comboBox
		# 
		self._inflow_par_comboBox.Anchor = System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._inflow_par_comboBox.DropDownHeight = 150
		self._inflow_par_comboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._inflow_par_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._inflow_par_comboBox.FormattingEnabled = True
		self._inflow_par_comboBox.IntegralHeight = False
		self._inflow_par_comboBox.ItemHeight = 16
		self._inflow_par_comboBox.Location = System.Drawing.Point(233, 258)
		self._inflow_par_comboBox.MaxDropDownItems = 10
		self._inflow_par_comboBox.Name = "inflow_par_comboBox"
		self._inflow_par_comboBox.Size = System.Drawing.Size(323, 24)
		self._inflow_par_comboBox.TabIndex = 13
		# 
		# run_button
		# 
		self._run_button.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right
		self._run_button.FlatAppearance.BorderColor = System.Drawing.Color.White
		self._run_button.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Gray
		self._run_button.Font = System.Drawing.Font("Microsoft Sans Serif", 14.25, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 204)
		self._run_button.Location = System.Drawing.Point(406, 330)
		self._run_button.Name = "run_button"
		self._run_button.Size = System.Drawing.Size(150, 35)
		self._run_button.TabIndex = 15
		self._run_button.Text = "RUN"
		self._run_button.UseVisualStyleBackColor = True
		# 
		# pars_set_groupBox
		# 
		self._pars_set_groupBox.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._pars_set_groupBox.Controls.Add(self._shr_pars_radio_button)
		self._pars_set_groupBox.Controls.Add(self._prj_pars_radio_button)
		self._pars_set_groupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._pars_set_groupBox.Location = System.Drawing.Point(12, 12)
		self._pars_set_groupBox.Name = "pars_set_groupBox"
		self._pars_set_groupBox.Size = System.Drawing.Size(348, 90)
		self._pars_set_groupBox.TabIndex = 0
		self._pars_set_groupBox.TabStop = False
		self._pars_set_groupBox.Text = "Choose Parameter Set"
		# 
		# prj_pars_radio_button
		# 
		self._prj_pars_radio_button.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left
		self._prj_pars_radio_button.Checked = True
		self._prj_pars_radio_button.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._prj_pars_radio_button.Location = System.Drawing.Point(28, 21)
		self._prj_pars_radio_button.Name = "prj_pars_radio_button"
		self._prj_pars_radio_button.Size = System.Drawing.Size(150, 44)
		self._prj_pars_radio_button.TabIndex = 0
		self._prj_pars_radio_button.TabStop = True
		self._prj_pars_radio_button.Text = "Project Parameters"
		self._prj_pars_radio_button.UseVisualStyleBackColor = True
		# 
		# shr_pars_radio_button
		# 
		self._shr_pars_radio_button.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right
		self._shr_pars_radio_button.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._shr_pars_radio_button.Location = System.Drawing.Point(182, 21)
		self._shr_pars_radio_button.Name = "shr_pars_radio_button"
		self._shr_pars_radio_button.Size = System.Drawing.Size(150, 44)
		self._shr_pars_radio_button.TabIndex = 1
		self._shr_pars_radio_button.Text = "Shared Parameters"
		self._shr_pars_radio_button.UseVisualStyleBackColor = True
		# 
		# shared_parameters_label
		# 
		self._shared_parameters_label.Anchor = System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._shared_parameters_label.AutoSize = True
		self._shared_parameters_label.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._shared_parameters_label.Location = System.Drawing.Point(4, 8)
		self._shared_parameters_label.Name = "shared_parameters_label"
		self._shared_parameters_label.Size = System.Drawing.Size(222, 20)
		self._shared_parameters_label.TabIndex = 0
		self._shared_parameters_label.Text = "Shared Parameters Group"
		self._shared_parameters_label.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# shared_parameters_comboBox
		# 
		self._shared_parameters_comboBox.Anchor = System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._shared_parameters_comboBox.Cursor = System.Windows.Forms.Cursors.Default
		self._shared_parameters_comboBox.DropDownHeight = 150
		self._shared_parameters_comboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._shared_parameters_comboBox.Enabled = False
		self._shared_parameters_comboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._shared_parameters_comboBox.FormattingEnabled = True
		self._shared_parameters_comboBox.IntegralHeight = False
		self._shared_parameters_comboBox.ItemHeight = 16
		self._shared_parameters_comboBox.Location = System.Drawing.Point(233, 6)
		self._shared_parameters_comboBox.MaxDropDownItems = 10
		self._shared_parameters_comboBox.Name = "shared_parameters_comboBox"
		self._shared_parameters_comboBox.Size = System.Drawing.Size(323, 24)
		self._shared_parameters_comboBox.TabIndex = 6
		# 
		# space_id_par_textBox
		# 
		self._space_id_par_textBox.Cursor = System.Windows.Forms.Cursors.No
		self._space_id_par_textBox.Dock = System.Windows.Forms.DockStyle.Fill
		self._space_id_par_textBox.Enabled = False
		self._space_id_par_textBox.Location = System.Drawing.Point(233, 76)
		self._space_id_par_textBox.Name = "space_id_par_textBox"
		self._space_id_par_textBox.Size = System.Drawing.Size(323, 20)
		self._space_id_par_textBox.TabIndex = 8
		self._space_id_par_textBox.Tag = "Space Identification Parameter"
		# 
		# pressure_cls_par_textBox
		# 
		self._pressure_cls_par_textBox.Cursor = System.Windows.Forms.Cursors.No
		self._pressure_cls_par_textBox.Dock = System.Windows.Forms.DockStyle.Fill
		self._pressure_cls_par_textBox.Enabled = False
		self._pressure_cls_par_textBox.Location = System.Drawing.Point(233, 148)
		self._pressure_cls_par_textBox.Name = "pressure_cls_par_textBox"
		self._pressure_cls_par_textBox.Size = System.Drawing.Size(323, 20)
		self._pressure_cls_par_textBox.TabIndex = 10
		self._pressure_cls_par_textBox.Tag = "Pressure Class Parameter"
		# 
		# overflow_par_textBox
		# 
		self._overflow_par_textBox.Cursor = System.Windows.Forms.Cursors.No
		self._overflow_par_textBox.Dock = System.Windows.Forms.DockStyle.Fill
		self._overflow_par_textBox.Enabled = False
		self._overflow_par_textBox.Location = System.Drawing.Point(233, 220)
		self._overflow_par_textBox.Name = "overflow_par_textBox"
		self._overflow_par_textBox.Size = System.Drawing.Size(323, 20)
		self._overflow_par_textBox.TabIndex = 12
		self._overflow_par_textBox.Tag = "Overflow Air Parameter"
		# 
		# inflow_par_textBox
		# 
		self._inflow_par_textBox.Cursor = System.Windows.Forms.Cursors.No
		self._inflow_par_textBox.Dock = System.Windows.Forms.DockStyle.Fill
		self._inflow_par_textBox.Enabled = False
		self._inflow_par_textBox.Location = System.Drawing.Point(233, 292)
		self._inflow_par_textBox.Name = "inflow_par_textBox"
		self._inflow_par_textBox.Size = System.Drawing.Size(323, 20)
		self._inflow_par_textBox.TabIndex = 14
		self._inflow_par_textBox.Tag = "Inflow Air Parameter"
		# 
		# door_pars_groupBox
		# 
		self._door_pars_groupBox.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right
		self._door_pars_groupBox.Controls.Add(self._flow_coeff_textBox)
		self._door_pars_groupBox.Controls.Add(self._flow_coeff_label)
		self._door_pars_groupBox.Controls.Add(self._door_crack_width_textBox)
		self._door_pars_groupBox.Controls.Add(self._door_crack_width_label)
		self._door_pars_groupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._door_pars_groupBox.Location = System.Drawing.Point(366, 12)
		self._door_pars_groupBox.Name = "door_pars_groupBox"
		self._door_pars_groupBox.Size = System.Drawing.Size(206, 90)
		self._door_pars_groupBox.TabIndex = 1
		self._door_pars_groupBox.TabStop = False
		self._door_pars_groupBox.Text = "Door Parameter"
		# 
		# door_crack_width_label
		# 
		self._door_crack_width_label.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left
		self._door_crack_width_label.AutoSize = True
		self._door_crack_width_label.Location = System.Drawing.Point(7, 22)
		self._door_crack_width_label.Name = "door_crack_width_label"
		self._door_crack_width_label.Size = System.Drawing.Size(130, 16)
		self._door_crack_width_label.TabIndex = 0
		self._door_crack_width_label.Text = "Door Crack Width, m"
		# 
		# door_crack_width_textBox
		# 
		self._door_crack_width_textBox.HideSelection = False
		self._door_crack_width_textBox.Location = System.Drawing.Point(154, 22)
		self._door_crack_width_textBox.Name = "door_crack_width_textBox"
		self._door_crack_width_textBox.Size = System.Drawing.Size(46, 22)
		self._door_crack_width_textBox.TabIndex = 1
		self._door_crack_width_textBox.Tag = "Door Crack Width"
		# 
		# flow_coeff_label
		# 
		self._flow_coeff_label.AutoSize = True
		self._flow_coeff_label.Location = System.Drawing.Point(7, 57)
		self._flow_coeff_label.Name = "flow_coeff_label"
		self._flow_coeff_label.Size = System.Drawing.Size(119, 16)
		self._flow_coeff_label.TabIndex = 2
		self._flow_coeff_label.Text = "Flow Coefficient (μ)"
		# 
		# flow_coeff_textBox
		# 
		self._flow_coeff_textBox.Location = System.Drawing.Point(154, 57)
		self._flow_coeff_textBox.Name = "flow_coeff_textBox"
		self._flow_coeff_textBox.Size = System.Drawing.Size(46, 22)
		self._flow_coeff_textBox.TabIndex = 3
		self._flow_coeff_textBox.Tag = "Flow Coefficient"
		# 
		# progressBar
		# 
		self._progressBar.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._progressBar.Location = System.Drawing.Point(12, 632)
		self._progressBar.Name = "progressBar"
		self._progressBar.Size = System.Drawing.Size(560, 23)
		self._progressBar.TabIndex = 4
		# 
		# settings_groupBox
		# 
		self._settings_groupBox.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._settings_groupBox.Controls.Add(self._save_stngs_button)
		self._settings_groupBox.Controls.Add(self._load_stngs_button)
		self._settings_groupBox.Controls.Add(self._config_file_path_textBox)
		self._settings_groupBox.Controls.Add(self._config_file_path_label)
		self._settings_groupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9.75, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 204)
		self._settings_groupBox.Location = System.Drawing.Point(12, 526)
		self._settings_groupBox.Name = "settings_groupBox"
		self._settings_groupBox.Size = System.Drawing.Size(560, 82)
		self._settings_groupBox.TabIndex = 3
		self._settings_groupBox.TabStop = False
		self._settings_groupBox.Text = "Settings"
		# 
		# config_file_path_label
		# 
		self._config_file_path_label.AutoSize = True
		self._config_file_path_label.Location = System.Drawing.Point(7, 20)
		self._config_file_path_label.Name = "config_file_path_label"
		self._config_file_path_label.Size = System.Drawing.Size(101, 16)
		self._config_file_path_label.TabIndex = 0
		self._config_file_path_label.Text = "Config File Path"
		# 
		# config_file_path_textBox
		# 
		self._config_file_path_textBox.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._config_file_path_textBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
		self._config_file_path_textBox.Enabled = False
		self._config_file_path_textBox.Location = System.Drawing.Point(7, 43)
		self._config_file_path_textBox.Name = "config_file_path_textBox"
		self._config_file_path_textBox.Size = System.Drawing.Size(287, 22)
		self._config_file_path_textBox.TabIndex = 1
		# 
		# load_stngs_button
		# 
		self._load_stngs_button.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right
		self._load_stngs_button.AutoSize = True
		self._load_stngs_button.Location = System.Drawing.Point(300, 41)
		self._load_stngs_button.Name = "load_stngs_button"
		self._load_stngs_button.Size = System.Drawing.Size(100, 26)
		self._load_stngs_button.TabIndex = 2
		self._load_stngs_button.Text = "Load Settings"
		self._load_stngs_button.UseVisualStyleBackColor = True
		# 
		# save_stngs_button
		# 
		self._save_stngs_button.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right
		self._save_stngs_button.AutoSize = True
		self._save_stngs_button.Location = System.Drawing.Point(406, 41)
		self._save_stngs_button.Name = "save_stngs_button"
		self._save_stngs_button.Size = System.Drawing.Size(101, 26)
		self._save_stngs_button.TabIndex = 3
		self._save_stngs_button.Text = "Save Settings"
		self._save_stngs_button.UseVisualStyleBackColor = True
		# 
		# MainForm
		# 
		self.ClientSize = System.Drawing.Size(584, 667)
		self.Controls.Add(self._settings_groupBox)
		self.Controls.Add(self._progressBar)
		self.Controls.Add(self._door_pars_groupBox)
		self.Controls.Add(self._pars_set_groupBox)
		self.Controls.Add(self._tableLayoutPanel)
		self.MinimumSize = System.Drawing.Size(600, 700)
		self.Name = "MainForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "Room Overflows"
		self._tableLayoutPanel.ResumeLayout(False)
		self._tableLayoutPanel.PerformLayout()
		self._pars_set_groupBox.ResumeLayout(False)
		self._door_pars_groupBox.ResumeLayout(False)
		self._door_pars_groupBox.PerformLayout()
		self._settings_groupBox.ResumeLayout(False)
		self._settings_groupBox.PerformLayout()
		self.ResumeLayout(False)
