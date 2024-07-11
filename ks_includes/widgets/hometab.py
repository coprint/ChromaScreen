from datetime import datetime
import logging
import os
import time

import gi
from matplotlib.patches import FancyBboxPatch
from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.widgets.keypad_new import KeyPadNew

gi.require_version("Gtk", "3.0")
from ks_includes.widgets.zaxistab import zAxisTab
from gi.repository import Gtk, GLib
import numpy as np
from matplotlib.backends.backend_gtk3agg import \
    FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("GTK3Agg")
class HomeTab(Gtk.Box):
    def __init__(self, this):
        super().__init__()
        self.sliderBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.sliderBox.set_halign(Gtk.Align.CENTER)
        self.startIndex = 0
        self.bodyBoxTotal = None
        self.systemTabBox = None
        self.staticTabBox = None
        self.axCanEnter = False
        self.cpu = 0
        self.mem = 0
        self.ax2 = None
        self.extruderLabel = Gtk.Label("0.0° / 0.0°", name="home-filament-box-input-label")
        self.this= this
        self.main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        #self.set_name("home-tab-box")
        self.tab1Button = Gtk.ToggleButton(label = _("Statistic"), name ="home-tab-title-label")
        self.tab1Button.set_active(True)
        self.tab1Button.connect("toggled", self.on_button_toggled, "1")
        self.tab2Button = Gtk.ToggleButton(label = _("System"), name ="home-tab-title-label")
        self.tab2Button.connect("toggled", self.on_button_toggled, "2")
        self.tab3Button = Gtk.ToggleButton(label = _("Filament"), name ="home-tab-title-label")
        self.tab3Button.connect("toggled", self.on_button_toggled, "3")

        printFilesTitlesBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        printFilesTitlesBox.set_name("home-tab-box-title")
        printFilesTitlesBox.set_valign(Gtk.Align.START) 
        printFilesTitlesBox.pack_start(self.tab1Button, False, False, 0)
        printFilesTitlesBox.pack_start(self.tab2Button, False, False, 0)
        printFilesTitlesBox.pack_start(self.tab3Button, False, False, 0)

        self.bodyBox =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.bodyBox.set_name("home-tab-box")
        self.bodyBox.set_valign(Gtk.Align.START)
        self.bodyBox.pack_start(Gtk.Label(_("Init..."),
                                             name="auto-leveling-content-label"), False, False, 0)
        contentBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        contentBox.pack_start(printFilesTitlesBox, False, False, 0)
        contentBox.pack_start(self.bodyBox, False, False, 0)
        self.add(contentBox)
        #self.connect("size-allocate", self.on_window_size_changed)


    def static_value(self):
        for child in self.bodyBox.get_children():
            self.bodyBox.remove(child)
        if self.staticTabBox == None:
            data = []
            for key in self.this.print_stats:
                data.append(key['value'])
            colors = ['#3E3E3E', '#ADADAD', '#5A5A5A', '#3E3E3E']
            fig = Figure(figsize=(6, 3), dpi=100)
            ax = fig.add_subplot()
            #fig, ax = plt.plot(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
            wedges,  texts = ax.pie(data, colors=colors, wedgeprops=dict(width=0.1), startangle=-40)
            kw = dict(arrowprops=dict(arrowstyle="-", color="w"),
                    zorder=0, va="center")
            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1)/2. + p.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = f"angle,angleA=0,angleB={ang}"
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                if "_" in self.this.print_stats[i]['name'] :
                    ax.annotate(_((self.this.print_stats[i]['name']).split('_')[1].capitalize()) + ': ' +str(int(self.this.print_stats[i]['value'])), color='w', 
                            xy=(x, y), xytext=(1.20*np.sign(x), 1.4*y),fontsize=7,
                            horizontalalignment=horizontalalignment, **kw)
                else: 
                    ax.annotate(_((self.this.print_stats[i]['name'].replace("_", " ")).capitalize()) + ': ' +str(int(self.this.print_stats[i]['value'])), color='w', 
                            xy=(x, y), xytext=(1.20*np.sign(x), 1.4*y),fontsize=7,
                            horizontalalignment=horizontalalignment, **kw)

            l = ax.legend(title='Total Job \n' + str(int(self.this.total_used['total_jobs'])), loc='center',facecolor='#0E0E0E', edgecolor='#0E0E0E')
            ax.get_legend().get_title().set_color('white')
            plt.setp(l.get_title(), multialignment='center')
            for text in texts:
                text.set_c('red')
            [text.set_c('red') for text in texts]
            ax.plot()
            canvas = FigureCanvas(fig)  # a Gtk.DrawingArea
            canvas.set_has_window(False)
            canvas.set_size_request(300, 188)
            fig.set_facecolor('#0E0E0E')
            fig2 = Figure(figsize=(6, 3), dpi=100)
            ax2 = fig2.add_subplot()
            days = []
            counts = []
            for usage in self.this.filament_usage_array:
                dt_object = datetime.fromtimestamp(usage[0])
                days.append(dt_object.day)
                counts.append(usage[1])
            colors2 = ['#63ABFD']
            ax2.bar(days, counts,  color=colors2, width=0.2)
            ax2.spines['bottom'].set_color('#4F4F4F')
            ax2.spines['top'].set_color('#4F4F4F')
            ax2.spines['right'].set_color('#4F4F4F')
            ax2.spines['left'].set_color('#4F4F4F')
            ax2.tick_params(axis='x', colors='white')      
            ax2.tick_params(axis='y', colors='white')
            ax2.set_axisbelow(True)      
            new_patches = []
            for patch in reversed(ax2.patches):
                bb = patch.get_bbox()
                color=patch.get_facecolor()
                p_bbox = FancyBboxPatch((bb.xmin, bb.ymin),
                                    abs(bb.width), abs(bb.height),
                                    boxstyle="round,pad=-0.0040,rounding_size=0.015",
                                    ec="none", fc=color,
                                    mutation_aspect=4
                                    )
                patch.remove()
                new_patches.append(p_bbox)
            for patch in new_patches:
                ax2.add_patch(patch)
            ax2.grid(zorder=-1, color = '#4F4F4F', linewidth = 0.5)
            ax2.set_facecolor("#0E0E0E")
            ax2.set(ylim=[0, 100])
            ax2.plot()
            canvas2 = FigureCanvas(fig2)
            canvas2.set_size_request(380, 188)
            canvas2.set_has_window(False)
            fig2.set_facecolor('#0E0E0E')
            mon, sec = divmod(self.this.total_used['total_print_time'], 60)
            hr, mon = divmod(mon, 60)
            label = ("%dh %02dm %02ds" % (hr, mon, sec))
            totalPrintTimeLabel = Gtk.Label(_("Total Print Time"), name="system-total-times-title-label")
            totalPrintTimeLabel.set_halign(Gtk.Align.START)
            totalPrintTimeValue = Gtk.Label(label, name="system-total-times-content-label")
            totalPrintTimeValue.set_halign(Gtk.Align.START)
            separatorTotalPrint = Gtk.HSeparator()
            separatorTotalPrint.get_style_context().add_class("tab-separator")
            
            bodyBoxTotalPrintTimeBox =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            bodyBoxTotalPrintTimeBox.set_valign(Gtk.Align.START)
            bodyBoxTotalPrintTimeBox.add(totalPrintTimeLabel)
            bodyBoxTotalPrintTimeBox.add(totalPrintTimeValue)
            bodyBoxTotalPrintTimeBox.add(separatorTotalPrint)
            bodyBoxTotalPrintTimeBox.set_name("tab-total-usabe-box")

            totalFilamentLabel = Gtk.Label(_("Total Filament Used"), name="system-total-times-title-label")
            totalFilamentLabel.set_halign(Gtk.Align.START)
            totalFilamentValue = Gtk.Label( "{:.1f}m".format( float(self.this.total_used['total_filament_used']/1000)) , name="system-total-times-content-label")
            totalFilamentValue.set_halign(Gtk.Align.START)
            separatorTotalFilament = Gtk.HSeparator()
            separatorTotalFilament.get_style_context().add_class("tab-separator")
            
            bodyBoxTotalFilament =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            bodyBoxTotalFilament.set_valign(Gtk.Align.START)
            bodyBoxTotalFilament.add(totalFilamentLabel)
            bodyBoxTotalFilament.add(totalFilamentValue)
            bodyBoxTotalFilament.add(separatorTotalFilament)
            bodyBoxTotalFilament.set_name("tab-total-usabe-box")

            bodyBoxTotal =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            bodyBoxTotal.add(bodyBoxTotalPrintTimeBox)
            bodyBoxTotal.add(canvas)
            bodyBoxGraphic =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            bodyBoxGraphic.add(bodyBoxTotalFilament)
            bodyBoxGraphic.add(canvas2)

            self.staticTabBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            self.staticTabBox.add(bodyBoxTotal)
            self.staticTabBox.add(bodyBoxGraphic)

        self.bodyBox.add(self.staticTabBox)
        self.bodyBox.show_all()

    def system_value(self):
        print(self.this.mcus)
        for child in self.bodyBox.get_children():
            self.bodyBox.remove(child)
        if self.systemTabBox == None:
            data = [self.this.instant_cpu, 100 - self.this.instant_cpu]
            colors = ['#7AD3FF', '#E6F5FD']
            self.fig = Figure(figsize=(6, 3), dpi=100)
            self.ax = self.fig.add_subplot()        
            wedges,  texts = self.ax.pie(data, colors=colors, wedgeprops=dict(width=0.2), startangle=-40)
            kw = dict(arrowprops=dict(arrowstyle="-", color="#0E0E0E"),
                    zorder=0, va="center")
            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1)/2. + p.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = f"angle,angleA=0,angleB={ang}"
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                self.ax.annotate('', color='b', xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                            horizontalalignment=horizontalalignment, **kw)
            l = self.ax.legend(title='%' +str(round(self.this.instant_cpu)), loc='center',facecolor='#0E0E0E', edgecolor='#0E0E0E')
            self.ax.get_legend().get_title().set_color('white')
            plt.setp(l.get_title(), multialignment='center')
            for text in texts:
                text.set_c('red')
            [text.set_c('red') for text in texts]
            self.canvas = FigureCanvas(self.fig)  # a Gtk.DrawingArea
            self.canvas.set_size_request(110, 110)
            self.fig.set_facecolor('#0E0E0E')
            grid = Gtk.Grid(column_homogeneous=True,
                            column_spacing=10,
                            row_spacing=10)
            row = 0
            count = 0
            for mcu in self.this.mcus:
                mcuLabel1 = Gtk.Label(f'{mcu["name"]}  ({mcu["chip"]})', name="system-content-title-label")
                mcuLabel1.set_halign(Gtk.Align.START)
                versionLabel1 = Gtk.Label(f'Version: {mcu["version"]}', name="system-content-label")
                versionLabel1.set_halign(Gtk.Align.START)
                loadLabel1 = Gtk.Label(f'Load: {mcu["load"]}, Awake: {mcu["awake"]}, Freq: {mcu["freqFormat"]}', name="system-content-label")
                loadLabel1.set_halign(Gtk.Align.START)
                leftTopContentBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                leftTopContentBox.set_valign(Gtk.Align.CENTER)
                leftTopContentBox.pack_start(mcuLabel1, False, False, 0)
                leftTopContentBox.pack_start(versionLabel1, False, False, 0)
                leftTopContentBox.pack_start(loadLabel1, False, False, 0)

                leftTopImage = self.this._gtk.Image("extrr", self.this._screen.width *.07, self.this._screen.width *.07)
                self.leftTopImageBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                self.leftTopImageBox.pack_start(self.canvas, False, False, 0)

                leftTopBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
                leftTopBox.pack_start(leftTopContentBox, False, False, 0)
                leftTopBox.pack_start(self.leftTopImageBox, False, False, 0)

                separator1 = Gtk.HSeparator()
                separator1.get_style_context().add_class("tab-separator")
                leftTopTotalBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                leftTopTotalBox.pack_start(leftTopBox, False, False, 0)
                leftTopTotalBox.pack_start(separator1, False, False, 0)
                
                grid.attach(leftTopTotalBox, count, row, 1, 1)
                count += 1
                if count % 2 is 0:
                    count = 0
                    row += 1

            data2 = [self.this.instant_mem, 100- self.this.instant_mem]
            colors2 = ['#7AD3FF', '#E6F5FD']
            fig2 = Figure(figsize=(6, 3), dpi=100)
            self.ax2 = fig2.add_subplot()
            wedges2,  texts2 = self.ax2.pie(data2, colors=colors2, wedgeprops=dict(width=0.2), startangle=-40)        
            kw2 = dict(arrowprops=dict(arrowstyle="-", color="#0E0E0E"),
                    zorder=0, va="center")
            for i, p in enumerate(wedges2):
                ang = (p.theta2 - p.theta1)/2. + p.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = f"angle,angleA=0,angleB={ang}"
                kw2["arrowprops"].update({"connectionstyle": connectionstyle})
                self.ax2.annotate('', color='b', xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                            horizontalalignment=horizontalalignment, **kw)
            l = self.ax2.legend(title='%' + str(round(self.this.instant_cpu)), loc='center',facecolor='#0E0E0E', edgecolor='#0E0E0E')
            self.ax2.get_legend().get_title().set_color('white')
            plt.setp(l.get_title(), multialignment='center')
            for text in texts:
                text.set_c('red')
            [text.set_c('red') for text in texts]
            self.canvas2 = FigureCanvas(fig2)  # a Gtk.DrawingArea
            self.canvas2.set_size_request(110, 110)
            fig2.set_facecolor('#0E0E0E')
            if self.this.hostInfo:
                host = self.this.hostInfo
                mcuLabel1 = Gtk.Label(f'Host   ({host.cpuName}, {host.bits})', name="system-content-title-label")
                mcuLabel1.set_halign(Gtk.Align.START)
                versionLabel1 = Gtk.Label(f'Version: {host.version}', name="system-content-label")
                versionLabel1.set_halign(Gtk.Align.START)
                versionLabel2 = Gtk.Label(f'OS: {host.os}', name="system-content-label")
                versionLabel2.set_halign(Gtk.Align.START)

                loadLabel1 = Gtk.Label(f'Load: {str(host.load)}, Mem: {host.memoryFormat}', name="system-content-label")
                loadLabel1.set_halign(Gtk.Align.START)

                leftTopContentBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                leftTopContentBox.set_valign(Gtk.Align.CENTER)
                leftTopContentBox.pack_start(mcuLabel1, False, False, 0)
                leftTopContentBox.pack_start(versionLabel1, False, False, 0)
                leftTopContentBox.pack_start(versionLabel2, False, False, 0)
                leftTopContentBox.pack_start(loadLabel1, False, False, 0)

                leftTopImage = self.this._gtk.Image("extrr", self.this._screen.width *.07, self.this._screen.width *.07)
                leftTopImageBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                leftTopImageBox.pack_start(self.canvas2, False, False, 0)

                leftTopBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
                leftTopBox.pack_start(leftTopContentBox, False, False, 0)
                leftTopBox.pack_start(leftTopImageBox, False, False, 0)

                separator1 = Gtk.HSeparator()
                separator1.get_style_context().add_class("tab-separator")
                leftTopTotalBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                leftTopTotalBox.pack_start(leftTopBox, False, False, 0)
                leftTopTotalBox.pack_start(separator1, False, False, 0)
                
                grid.attach(leftTopTotalBox, count, row, 1, 1)
                count += 1
                if count % 2 is 0:
                    count = 0
                    row += 1

            gridBox = Gtk.Box()
            gridBox.set_halign(Gtk.Align.CENTER)
            gridBox.add(grid)
            #-----system restart button-----#
            systemRestartIcon = self.this._gtk.Image("redo", 30, 30)
            systemRestartLabel = Gtk.Label(_("System Restart"), name="system-tab-button-label")            
            systemRestartBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            systemRestartBox.set_halign(Gtk.Align.CENTER)
            systemRestartBox.set_valign(Gtk.Align.CENTER)
            systemRestartBox.pack_start(systemRestartIcon, False, False, 0)
            systemRestartBox.pack_start(systemRestartLabel, False, False, 0)
            self.systemRestartButton = Gtk.Button(name ="system-restart-tab-blue-button")
            self.systemRestartButton.add(systemRestartBox)
            self.systemRestartButton.connect("clicked", self.on_click_system_restart)
            self.systemRestartButton.set_always_show_image (True)
            #-----firmware restart button-----#
            firmwareRestartIcon = self.this._gtk.Image("reload", 30, 30)
            firmwareRestartLabel = Gtk.Label(_("Firmware Restart"), name="system-tab-button-label")            
            firmwareRestartBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            firmwareRestartBox.set_halign(Gtk.Align.CENTER)
            firmwareRestartBox.set_valign(Gtk.Align.CENTER)
            firmwareRestartBox.pack_start(firmwareRestartIcon, False, False, 0)
            firmwareRestartBox.pack_start(firmwareRestartLabel, False, False, 0)
            self.firmwareRestartButton = Gtk.Button(name ="system-restart-tab-red-button")
            self.firmwareRestartButton.add(firmwareRestartBox)
            self.firmwareRestartButton.connect("clicked", self.on_click_firmware_restart)
            self.firmwareRestartButton.set_always_show_image (True)
            restartBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)     
            restartBox.pack_start(self.systemRestartButton, False, False, 0)
            restartBox.pack_start(self.firmwareRestartButton, False, False, 0)
            #-----shutdown button-----#
            shutdownIcon = self.this._gtk.Image("power", 30, 30)
            shutdownLabel = Gtk.Label(_("Shutdown"), name="system-tab-button-label")            
            shutdownBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            shutdownBox.set_halign(Gtk.Align.CENTER)
            shutdownBox.set_valign(Gtk.Align.CENTER)
            shutdownBox.pack_start(shutdownIcon, False, False, 0)
            shutdownBox.pack_start(shutdownLabel, False, False, 0)
            self.shutdownButtonButton = Gtk.Button(name ="system-shutdown-tab-grey-button")
            self.shutdownButtonButton.add(shutdownBox)
            #self.shutdownButtonButton.connect("clicked", self.on_click_firmware_restart)
            self.shutdownButtonButton.connect("clicked", self.reboot_poweroff, "poweroff")
            self.shutdownButtonButton.set_always_show_image (True)
            bodyBoxButton = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            bodyBoxButton.add(restartBox)
            bodyBoxButton.pack_end(self.shutdownButtonButton, False, False, 0)
            #bodyBoxButton.add(leftBottomTotalBox)
            self.systemTabBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.systemTabBox.add(gridBox)
            #systemTabBox.add(bodyBoxGraphic)
            self.systemTabBox.add(bodyBoxButton)
        
        self.bodyBox.add(self.systemTabBox)
        self.this.content.show_all()
        self.axCanEnter = True

    def updateCPU(self, cpu):
        if self.axCanEnter and round(self.cpu) != round(cpu):
            self.cpu = cpu    
            data = [cpu, 100-cpu]
            colors = ['#7AD3FF', '#E6F5FD']
            wedges,  texts = self.ax.pie(data, colors=colors, wedgeprops=dict(width=0.2), startangle=-40)
            kw = dict(arrowprops=dict(arrowstyle="-", color="#0E0E0E"),
                    zorder=0, va="center")
            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1)/2. + p.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
            
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = f"angle,angleA=0,angleB={ang}"
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                self.ax.annotate('', color='b', xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                            horizontalalignment=horizontalalignment, **kw)
            l = self.ax.legend(title='%' + str(round(cpu)), loc='center',facecolor='#0E0E0E', edgecolor='#0E0E0E')
            self.ax.get_legend().get_title().set_color('white')
            plt.setp(l.get_title(), multialignment='center')
            for text in texts:
                text.set_c('red')
            [text.set_c('red') for text in texts]
            plt.ion()
            self.canvas.draw()
          
    def updateMEM(self, mem):
            if self.axCanEnter and round(self.mem) != round(mem):
                self.mem = mem    
                data = [mem, 100-mem]
                colors = ['#7AD3FF', '#E6F5FD']            
                wedges,  texts = self.ax2.pie(data, colors=colors, wedgeprops=dict(width=0.2), startangle=-40)
                kw = dict(arrowprops=dict(arrowstyle="-", color="#0E0E0E"),
                        zorder=0, va="center")
                for i, p in enumerate(wedges):
                    ang = (p.theta2 - p.theta1)/2. + p.theta1
                    y = np.sin(np.deg2rad(ang))
                    x = np.cos(np.deg2rad(ang))
                    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                    connectionstyle = f"angle,angleA=0,angleB={ang}"
                    kw["arrowprops"].update({"connectionstyle": connectionstyle})
                    self.ax2.annotate('', color='b', xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                                horizontalalignment=horizontalalignment, **kw)
                l = self.ax2.legend(title='%' + str(round(mem)), loc='center',facecolor='#0E0E0E', edgecolor='#0E0E0E')
                self.ax2.get_legend().get_title().set_color('white')
                plt.setp(l.get_title(), multialignment='center')
                for text in texts:
                    text.set_c('red')
                [text.set_c('red') for text in texts]
                plt.ion()
                self.canvas2.draw()
        
    def filament_value(self):
        for child in self.bodyBox.get_children():
            self.bodyBox.remove(child)
        if self.bodyBoxTotal == None:
            #---- GREEN BUTTON BOX -----#
            # oneButtonLabel = Gtk.Label("Parked", name="parked-label")
            # twoButtonLabel = Gtk.Label("Parked", name="parked-label")
            # threeButtonLabel = Gtk.Label("Parked", name="parked-label")
            # fourButtonLabel = Gtk.Label("Parked", name="parked-label")

            # self.oneButton = Gtk.Button('1',name ="filament-tab-black-button")
            # #self.oneButton.connect("clicked", self.manuel_level, 1)
            # oneButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            # oneButtonBox.set_name("filament-tab-greeen-button-box")
            # oneButtonBox.set_halign(Gtk.Align.CENTER)
            # oneButtonBox.pack_start(self.oneButton, False, False, 0)
            # oneButtonBoxWithLabel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            # oneButtonBoxWithLabel.pack_start(oneButtonLabel, False, False, 0)
            # oneButtonBoxWithLabel.pack_start(oneButtonBox, False, False, 0)

            # self.twoButton = Gtk.Button('2',name ="filament-tab-black-button")
            # #self.twoButton.connect("clicked", self.manuel_level, 1)
            # twoButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            # twoButtonBox.set_name("filament-tab-greeen-button-box")
            # twoButtonBox.set_halign(Gtk.Align.CENTER)
            # twoButtonBox.pack_start(self.twoButton, False, False, 0)
            # twoButtonBoxWithLabel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            # twoButtonBoxWithLabel.pack_start(twoButtonLabel, False, False, 0)
            # twoButtonBoxWithLabel.pack_start(twoButtonBox, False, False, 0)

            # self.threeButton = Gtk.Button('3',name ="filament-tab-black-button")
            # #self.threeButton.connect("clicked", self.manuel_level, 1)
            # threeButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            # threeButtonBox.set_name("filament-tab-greeen-button-box")
            # threeButtonBox.set_halign(Gtk.Align.CENTER)
            # threeButtonBox.pack_start(self.threeButton, False, False, 0)
            # threeButtonBoxWithLabel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            # threeButtonBoxWithLabel.pack_start(threeButtonLabel, False, False, 0)
            # threeButtonBoxWithLabel.pack_start(threeButtonBox, False, False, 0)

            # self.fourButton = Gtk.Button('4',name ="filament-tab-black-button")
            # #self.fourButton.connect("clicked", self.manuel_level, 1)
            # fourButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            # fourButtonBox.set_name("filament-tab-greeen-button-box")
            # fourButtonBox.set_halign(Gtk.Align.CENTER)
            # fourButtonBox.pack_start(self.fourButton, False, False, 0)
            # fourButtonBoxWithLabel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            # fourButtonBoxWithLabel.pack_start(fourButtonLabel, False, False, 0)
            # fourButtonBoxWithLabel.pack_start(fourButtonBox, False, False, 0)

            nextIcon = self.this._gtk.Image("forward-arrow", 30, 30)
            self.nextButton = Gtk.Button(name ="directivity-button")
            self.nextButton.add(nextIcon)
            self.nextButton.connect("clicked", self.show_next_page)
            self.nextButton.set_always_show_image (True)   
            nextButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            nextButtonBox.pack_start(self.nextButton, False, False, 0)

            prevIcon = self.this._gtk.Image("back-arrow", 30, 30)
            self.prevButton = Gtk.Button(name ="directivity-button")
            self.prevButton.add(prevIcon)
            self.prevButton.connect("clicked", self.show_prev_page)
            self.prevButton.set_always_show_image (True) 
            prevButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            prevButtonBox.pack_start(self.prevButton, False, False, 0)

            greenButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            #greenButtonBox.pack_start(prevButtonBox, False, False, 0)
            greenButtonBox.pack_start(self.generateBoxs(),False, False, 0)
            fixed = Gtk.Fixed()
            fixed.set_valign(Gtk.Align.START)
            fixed.set_halign(Gtk.Align.START)
            fixed.put(greenButtonBox, 58, 10)
            fixed.put(prevButtonBox, 0, 38)
            fixed.put(nextButtonBox, 372, 38)
            # greenButtonBox.pack_start(oneButtonBoxWithLabel, False, False, 0)
            # greenButtonBox.pack_start(twoButtonBoxWithLabel, False, False, 0)
            # greenButtonBox.pack_start(threeButtonBoxWithLabel, False, False, 0)
            # greenButtonBox.pack_start(fourButtonBoxWithLabel, False, False, 0)
            #greenButtonBox.pack_start(nextButtonBox, False, False, 0)
            #---- LOAD - UNLOAD BUTTON BOX ----#
            downloadIcon = self.this._gtk.Image("download-white", 20, 20)
            loadLabel = Gtk.Label(_("Load"), name="load-unload-label")            
            loadButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            loadButtonBox.set_name("load-unload-button-box")
            loadButtonBox.set_halign(Gtk.Align.CENTER)
            loadButtonBox.set_valign(Gtk.Align.CENTER)
            loadButtonBox.pack_start(downloadIcon, False, False, 0)
            loadButtonBox.pack_start(loadLabel, False, False, 0)
            self.loadButton = Gtk.Button(name ="home-tab-filament-cut-button")
            self.loadButton.add(loadButtonBox)
            self.loadButton.connect("clicked", self.load)
            self.loadButton.set_always_show_image (True)
            loadButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            loadButtonBox.set_valign(Gtk.Align.CENTER)
            loadButtonBox.set_halign(Gtk.Align.CENTER)
            loadButtonBox.pack_start(self.loadButton, False, False, 0)

            unLoadIcon = self.this._gtk.Image("upload", 20, 20)
            unloadLabel = Gtk.Label(_("Park"), name="load-unload-label")            
            unloadButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            unloadButtonBox.set_name("load-unload-button-box")
            unloadButtonBox.set_halign(Gtk.Align.CENTER)
            unloadButtonBox.set_valign(Gtk.Align.CENTER)
            unloadButtonBox.pack_start(unLoadIcon, False, False, 0)
            unloadButtonBox.pack_start(unloadLabel, False, False, 0)
            self.unloadButton = Gtk.Button(name ="home-tab-filament-cut-button")
            self.unloadButton.add(unloadButtonBox)
            self.unloadButton.connect("clicked", self.unload)
            self.unloadButton.set_always_show_image (True)
            unloadButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            unloadButtonBox.set_valign(Gtk.Align.CENTER)
            unloadButtonBox.set_halign(Gtk.Align.CENTER)
            unloadButtonBox.pack_start(self.unloadButton, False, False, 0)

            filamentImage = self.this._gtk.Image("filament-image", 75, 75)
            filamentImageBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            filamentImageBox.pack_start(filamentImage, False, False, 0)
       
            filamentSensor = ""
            detectedFilament = False
            for x in self.this._printer.get_filament_sensors():
                if self.this._printer.get_stat(x, "enabled"):
                    if self.this._printer.data[x]['filament_detected']:
                        detectedFilament = True
                if detectedFilament:
                    filamentSensor = self.this._gtk.Image("active-filament-sensor", 40, 40)
                else:
                    filamentSensor = self.this._gtk.Image("filament-sensor", 40, 40)
            filamentSensorBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            if filamentSensor != "" :
                filamentSensorBox.pack_start(filamentSensor, True, True, 0)

            loadUnloadButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            loadUnloadButtonBox.set_valign(Gtk.Align.CENTER)
            loadUnloadButtonBox.set_halign(Gtk.Align.CENTER)
            loadUnloadButtonBox.pack_start(loadButtonBox, False, False, 0)
            loadUnloadButtonBox.pack_start(filamentImageBox, False, False, 0)
            loadUnloadButtonBox.pack_start(filamentSensorBox, False, False, 0)
            loadUnloadButtonBox.pack_start(unloadButtonBox, False, False, 0)
            #----input box----#
            numPadIconExtruder = self.this._gtk.Image("calculator", self.this._screen.width *.03, self.this._screen.width *.03)
            numPadButtonExtruder = Gtk.Button(name ="speed-factor-button")
            numPadButtonExtruder.connect("clicked", self.open_numpad)
            numPadButtonExtruder.set_image(numPadIconExtruder)
            numPadButtonExtruder.set_always_show_image(True)
            #extruder
            self.extruderLabel = Gtk.Label("0.0° / 0.0°", name="home-filament-box-input-label")
            extruderLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            extruderLabelBox.set_name("temperature-label-box")
            extruderLabelBox.set_valign(Gtk.Align.CENTER)
            extruderLabelBox.set_halign(Gtk.Align.CENTER)
            extruderLabelBox.pack_start(self.extruderLabel, False, False, 0)
            extruderLabelBox.pack_end(numPadButtonExtruder, False, False, 0)
            
            downIcon = self.this._gtk.Image("eksi", self.this._screen.width *.02, self.this._screen.width *.02)
            upIcon = self.this._gtk.Image("arti", self.this._screen.width *.02, self.this._screen.width *.02)
            
            upButton = Gtk.Button(name ="scale-buttons")
            upButton.set_image(upIcon)
            upButton.set_always_show_image(True)
            upButton.connect("clicked", self.up_down_button_clicked, "extruder", "+")
            
            downButton = Gtk.Button(name ="scale-buttons")
            downButton.set_image(downIcon)
            downButton.set_always_show_image(True)
            downButton.connect("clicked", self.up_down_button_clicked, "extruder", "-")
        
            extruderInputBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
            extruderInputBox.set_valign(Gtk.Align.CENTER)
            extruderInputBox.set_halign(Gtk.Align.CENTER)
            extruderInputBox.pack_start(downButton, True, True, 0)
            extruderInputBox.pack_start(extruderLabelBox, True, True, 0)
            extruderInputBox.pack_start(upButton, True, True, 0)

            
            leftFilamentBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
            leftFilamentBox.pack_start(fixed, False, False, 0)
            leftFilamentBox.pack_start(loadUnloadButtonBox, True, True, 0)
            #leftFilamentBox.pack_start(extruderInputBox, False, False, 0)

            filamentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            filamentBox.set_name("filament-tab-box")
            filamentBox.pack_start(leftFilamentBox, False, False, 0)
            ###########################
            self.extruderImage = self.this._gtk.Image("extrr", self.this._screen.width *.05, self.this._screen.width *.05)
            switchWithImageBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            switchWithImageBox.set_halign(Gtk.Align.CENTER)
            switchWithImageBox.add(self.extruderImage)
        
            extrudeBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            extrudeBox.set_valign(Gtk.Align.CENTER)
            extrudeBox.pack_start(switchWithImageBox, False, False, 0)
            #self.distanceLabel = Gtk.Label(self.distance, name="number-label")
            self.distanceLabel = Gtk.Label("50", name="number-label")
        
            numberLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            numberLabelBox.set_valign(Gtk.Align.CENTER)
            numberLabelBox.set_halign(Gtk.Align.CENTER)
            numberLabelBox.set_name("number-label-box")
            numberLabelBox.add(self.distanceLabel)
            
            InputBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            InputBox.set_valign(Gtk.Align.CENTER)
            InputBox.set_halign(Gtk.Align.CENTER)
            InputBox.pack_start(numberLabelBox, True, True, 0)
            #InputBox.pack_start(numPadButton, True, True, 0)
            extrudeBox.pack_start(InputBox, False, False, 0)
            
            Extrude = zAxisTab(self.this, "", False)
            ExtrudeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            ExtrudeBox.pack_start(Extrude, False, False, 0)
            ExtrudeBox.set_halign(Gtk.Align.CENTER)
            ExtrudeBox.set_valign(Gtk.Align.CENTER)
            extrudeBox.pack_start(ExtrudeBox, False, False, 0)
            
            
            extrudeBox_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            extrudeBox_box.set_halign(Gtk.Align.CENTER)
            extrudeBox_box.set_valign(Gtk.Align.CENTER)
            extrudeBox_box.pack_start(extrudeBox, False, False, 0)
            #####################################################
            self.coolDownButton = Gtk.Button(_("Cooldown"), name ="home-tab-filament-cut-button")
            self.coolDownButton.connect("clicked", self.this.set_temperature,  'cooldown')
            self.disableStepperButton = Gtk.Button(_("Filament Cut"), name ="home-tab-filament-cut-button")
            self.disableStepperButton.connect("clicked", self.this.filament_cut)

            buttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            buttonBox.pack_start(self.coolDownButton, False, False, 0)
            buttonBox.pack_start(self.disableStepperButton, False, False, 0)
            
            self.bodyBoxTotal =  Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            self.bodyBoxTotal.pack_start(filamentBox, False, False, 0)
            self.bodyBoxTotal.pack_start(extrudeBox_box, False, False, 0)
            self.bodyBoxTotal.pack_start(buttonBox, False, False, 0)
        self.bodyBox.add(self.bodyBoxTotal)
        self.this.content.show_all()
    
    def show_next_page(self, widget):
        self.startIndex = self.startIndex +4
        if self.startIndex > 16:
            self.startIndex = 16
        self.generateBoxs()

    def show_prev_page(self, widget):
        if self.startIndex <= 4:
            self.startIndex = 0
        else:
            self.startIndex = (self.startIndex - 4)
        self.generateBoxs()

    def active(self, eventBox ,  gparam,  extruder):
        for i, item in enumerate(self.this.extruders):
            if item['Extrude'] != extruder['Extrude']:
                item['EventBox'].get_style_context().remove_class("filament-extruder-active")
            else:
                self.this._printer.selectedExtruder = extruder['Extrude']
                item['EventBox'].get_style_context().add_class("filament-extruder-active")
                self.this._screen._ws.klippy.gcode_script("T" + str(i))
                
    def generateBoxs(self):
        if self.sliderBox.get_children() != None:
            for child in self.sliderBox.get_children():
                self.sliderBox.remove(child)
        grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=10,
                         row_spacing=10)
        count = 0
        for extruder in self.this.extruders[self.startIndex: self.startIndex+4]:
            extruderLabel = ""
            extruder['Image'] = self.this._gtk.Image(extruder['Name'], self.this._gtk.content_width * .10 , self.this._gtk.content_height * .10)
            if extruder['FilamentStatus']== 'Unloaded':
                extruderLabel = Gtk.Label("UnLoaded", name="unloaded-label")
            elif extruder['FilamentStatus']== 'Parked':
                extruderLabel = Gtk.Label("Parked", name="parked-label")
            elif extruder['FilamentStatus']== 'Loaded':
                extruderLabel = Gtk.Label("Loaded", name="loaded-label")
            alignment = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            alignment.set_halign(Gtk.Align.CENTER)
            alignment.add(extruderLabel)
            extruderBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            extruderBox.set_name("extruder-filament-select-box ")
            extruderBox.set_halign(Gtk.Align.CENTER)
            extruderBox.set_valign(Gtk.Align.CENTER)
            extruderBox.pack_start(alignment, False, True, 5)
            extruderBox.pack_start(extruder['Image'], False, True, 5)
            eventBox = Gtk.EventBox()
            eventBox.add(extruderBox)
            extruder['EventBox'] = Gtk.Frame(name= "filament-extruder")
            extruder['EventBox'].add(eventBox)
            if extruder['Extrude'] != self.this._printer.selectedExtruder:
                extruder['EventBox'].get_style_context().remove_class("filament-extruder-active")
            else:
                extruder['EventBox'].get_style_context().add_class("filament-extruder-active")
            if extruder['RadioButtonStatus']:
                extruder['EventBox'].connect("button-press-event", self.this.chanceExtruder, extruder['Extrude'])
            grid.attach(extruder['EventBox'], count, 0, 1, 1)
            count += 1

        gridBox = Gtk.Box()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)
        self.sliderBox.pack_start(gridBox,False, False,0)
        self.sliderBox.show_all()
        return self.sliderBox or  True

    def load(self,widget):
        detectedFilament = False
        for x in self.this._printer.get_filament_sensors():
            if x in self.this._printer.data:
                 if 'filament_detected' in self.this._printer.data[x]:
                    if self.this._printer.data[x]['filament_detected']:
                        logging.info(f"{x}")
                        detectedFilament = True
        if detectedFilament:
            self.this._screen.show_popup_message("there is Loaded Filament")
        else:
            self.this._screen._ws.klippy.gcode_script(KlippyGcodes.LOAD_FILAMENT)
            for i, item in enumerate(self.this.extruders):
                if item['Extrude'] == self.this._printer.selectedExtruder :
                    item['FilamentStatus'] = 'Loaded'
            self.generateBoxs()

    def unload(self,widget):
        detectedFilament = False
        for x in self.this._printer.get_filament_sensors():
            if x in self.this._printer.data:
                 if 'filament_detected' in self.this._printer.data[x]:
                    if self.this._printer.data[x]['filament_detected']:
                        detectedFilament = True
        if detectedFilament:
            for i, item in enumerate(self.this.extruders):
                if item['Extrude'] == self.this._printer.selectedExtruder :
                    #if item['FilamentStatus'] == 'Loaded':
                    self.this._screen._ws.klippy.gcode_script(KlippyGcodes.PARK_FILAMENT)
                    item['FilamentStatus'] = 'Parked'
                else:
                    if item['FilamentStatus'] == 'Loaded':
                        self.this._screen.show_popup_message("the {item['Extrude']} is Loaded")
        else:
            self.this._screen._ws.klippy.gcode_script(KlippyGcodes.PARK_FILAMENT)
            for i, item in enumerate(self.this.extruders):
                if item['Extrude'] == self.this._printer.selectedExtruder :
                    item['FilamentStatus'] = 'Parked'
                else:
                    if  item['FilamentStatus'] == 'Loaded':
                        item['FilamentStatus'] = 'Parked'
        self.generateBoxs()

    def reboot_poweroff(self, widget, method):
        scroll = self.this._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)
        if method == "reboot":
            label = Gtk.Label(label=_("Are you sure you wish to reboot the system?"))
        else:
            label = Gtk.Label(label=_("Are you sure you wish to shutdown the system?"))
        vbox.add(label)
        scroll.add(vbox)
        buttons = [
            {"name": _("Ok"), "response": Gtk.ResponseType.OK},
            {"name": _("Cancel"), "response": Gtk.ResponseType.CANCEL}
        ]
        dialog = self.this._gtk.Dialog(self.this._screen, buttons, scroll, self.reboot_poweroff_confirm, method)
        if method == "reboot":
            dialog.set_title(_("Restart"))
        else:
            dialog.set_title(_("Shut Down"))

    def reboot_poweroff_confirm(self, dialog, response_id, method):
        self.this._gtk.remove_dialog(dialog)
        if response_id == Gtk.ResponseType.OK:
            if method == "reboot":
                os.system("systemctl reboot")
            else:
                os.system("systemctl poweroff")
        elif response_id == Gtk.ResponseType.APPLY:
            if method == "reboot":
                self.this._screen._ws.send_method("machine.reboot")
            else:
                self.this._screen._ws.send_method("machine.shutdown")

    def on_click_system_restart(self, button):        
        self.this._screen._ws.klippy.restart()
    
    def on_click_firmware_restart(self, button):
        self.this._screen._ws.klippy.restart_firmware()

    def updateValue(self, label):
        self.extruderLabel.set_text(label)

    def open_numpad(self, widget):
        dialog = KeyPadNew(self.this)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            self.this.change_extruder_temperature_pre(int(dialog.resp))
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        dialog.destroy()   

    def up_down_button_clicked(self, widget, tempType , direction):
        self.constant = 10
        value =0
        if(direction =="+"):
            if(tempType== "extruder"):
                value = self.this.extruder_temp_target + self.constant
            else:
                value = self.this.heater_bed_temp_target + self.constant
        else:
            if(tempType== "extruder"):
                value = self.this.extruder_temp_target - self.constant
            else:
                value = self.this.heater_bed_temp_target - self.constant
        if (value < 0):
            value = 0
        self.this.change_extruder_temperature(value)
              
    def on_button_toggled(self, button, name):
        if button.get_active():
            if name == "1": 
                self.tab1Button.set_active(True)
                self.tab2Button.set_active(False)
                self.tab3Button.set_active(False)
                self.axCanEnter = False
                self.static_value()
            if name == "2":
                self.tab1Button.set_active(False)
                self.tab2Button.set_active(True)
                self.tab3Button.set_active(False)
                self.axCanEnter = True
                self.system_value()
            if name == "3":
                self.tab1Button.set_active(False)
                self.tab2Button.set_active(False)
                self.tab3Button.set_active(True)
                self.axCanEnter = False
                self.filament_value()