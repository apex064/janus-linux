import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import subprocess
import threading
import requests
import os
import time

BACKUP_FOLDER = os.path.expanduser("~/Linux3uToolsBackups")
MOUNT_POINT = os.path.expanduser("~/Linux3uToolsMount")

class Linux3uTools(Gtk.Window):
    def __init__(self):
        super().__init__(title="Linux3uTools")
        self.set_default_size(1000, 700)

        notebook = Gtk.Notebook()
        self.add(notebook)

        # ---------------- Device Info Tab ----------------
        self.device_store = Gtk.ListStore(str, str)
        self.device_tree = Gtk.TreeView(model=self.device_store)
        renderer_text = Gtk.CellRendererText()
        self.device_tree.append_column(Gtk.TreeViewColumn("Field", renderer_text, text=0))
        self.device_tree.append_column(Gtk.TreeViewColumn("Value", renderer_text, text=1))

        device_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.device_tree)
        device_box.pack_start(scroll, True, True, 0)

        button_box = Gtk.Box(spacing=10)
        self.refresh_button = Gtk.Button(label="Refresh Info")
        self.refresh_button.connect("clicked", self.refresh_device_info)
        self.activate_button = Gtk.Button(label="Activate Device")
        self.activate_button.set_sensitive(False)
        self.activate_button.connect("clicked", self.start_activation)
        button_box.pack_start(self.refresh_button, True, True, 0)
        button_box.pack_start(self.activate_button, True, True, 0)
        device_box.pack_start(button_box, False, False, 0)

        self.status_label = Gtk.Label(label="Status: Not Checked")
        device_box.pack_start(self.status_label, False, False, 0)

        notebook.append_page(device_box, Gtk.Label(label="Device Info"))

        # ---------------- Activation Tab ----------------
        activation_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.activation_status_label = Gtk.Label(label="Activation Status: Not Checked")
        activation_box.pack_start(self.activation_status_label, False, False, 5)

        activate_tab_btn = Gtk.Button(label="Activate Device")
        activate_tab_btn.connect("clicked", self.start_activation)
        activation_box.pack_start(activate_tab_btn, False, False, 5)
        notebook.append_page(activation_box, Gtk.Label(label="Activation"))

        # ---------------- Backup/Restore Tab ----------------
        backup_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.backup_status = Gtk.Label(label="Backup/Restore Status: Idle")
        backup_box.pack_start(self.backup_status, False, False, 5)

        create_backup_btn = Gtk.Button(label="Create Backup")
        create_backup_btn.connect("clicked", self.create_backup)
        restore_backup_btn = Gtk.Button(label="Restore Backup")
        restore_backup_btn.connect("clicked", self.restore_backup)
        backup_box.pack_start(create_backup_btn, False, False, 5)
        backup_box.pack_start(restore_backup_btn, False, False, 5)
        notebook.append_page(backup_box, Gtk.Label(label="Backup/Restore"))

        # ---------------- File Manager Tab ----------------
        file_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.file_status_label = Gtk.Label(label="File Manager Status: Idle")
        file_box.pack_start(self.file_status_label, False, False, 5)

        mount_btn = Gtk.Button(label="Mount Filesystem")
        mount_btn.connect("clicked", self.mount_filesystem)
        unmount_btn = Gtk.Button(label="Unmount Filesystem")
        unmount_btn.connect("clicked", self.unmount_filesystem)
        file_box.pack_start(mount_btn, False, False, 5)
        file_box.pack_start(unmount_btn, False, False, 5)
        notebook.append_page(file_box, Gtk.Label(label="File Manager"))

        self.show_all()

        # Initial fetch
        threading.Thread(target=self.fetch_device_info).start()
        GLib.timeout_add(2000, self.check_sn_in_background)

    # ---------------- Command Executor ----------------
    def execute_command(self, command, *args):
        try:
            result = subprocess.run([command] + list(args), capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"

    # ---------------- Device Info ----------------
    def fetch_device_info(self):
        output = self.execute_command("ideviceinfo")
        info_dict = {}
        for line in output.splitlines():
            if ": " in line:
                key, value = line.split(": ", 1)
                info_dict[key.strip()] = value.strip()
        GLib.idle_add(self.update_device_tree, info_dict)

    def update_device_tree(self, info_dict):
        self.device_store.clear()
        categories = [
            ("Basic Info", ["DeviceName", "ProductType", "ProductVersion", "SerialNumber"]),
            ("Hardware", ["HardwareModel", "CPUArchitecture", "ChipID", "UniqueChipID"]),
            ("Network", ["WiFiAddress", "BluetoothAddress", "EthernetAddress"]),
            ("SIM Info", ["PhoneNumber", "SIMStatus", "CarrierBundleInfoArray[1].CFBundleIdentifier"]),
            ("Activation", ["ActivationState", "ActivationStateAcknowledged"]),
            ("Baseband", ["BasebandVersion", "BasebandStatus"])
        ]
        for category, fields in categories:
            self.device_store.append([f"--- {category} ---", ""])
            for field in fields:
                self.device_store.append([field, info_dict.get(field, "")])

    def refresh_device_info(self, button):
        self.status_label.set_text("Refreshing device info...")
        self.activate_button.set_sensitive(False)
        threading.Thread(target=self.fetch_device_info).start()
        GLib.timeout_add(2000, self.check_sn_in_background)

    # ---------------- Activation ----------------
    def check_sn_in_background(self):
        def task():
            sn = self.execute_command("ideviceinfo", "-k", "SerialNumber")
            if not sn:
                GLib.idle_add(self.show_error, "Device not connected.")
                return False
            try:
                url = f"https://a12janusunion.cloud/J12A/tentaAE/A12BChecker.php?sn={sn}"
                response = requests.get(url, timeout=10).text.strip()
                if response == "authorized":
                    GLib.idle_add(self.activate_button.set_sensitive, True)
                    GLib.idle_add(self.status_label.set_text, "Status: Device Authorized")
                else:
                    GLib.idle_add(self.show_error, "Unauthorized device.")
            except Exception as e:
                GLib.idle_add(self.show_error, f"Network error: {e}")
            return False
        threading.Thread(target=task).start()
        return False

    def start_activation(self, button):
        self.status_label.set_text("Starting activation...")
        self.activate_button.set_sensitive(False)
        threading.Thread(target=self.activation_task).start()

    def activation_task(self):
        self.execute_command("ideviceactivation", "activate", "-s", "https://a12janusunion.cloud/J12A/monstrinho.php")
        GLib.timeout_add_seconds(15, self.check_activation_status)

    def check_activation_status(self):
        state = self.execute_command("ideviceinfo", "-k", "ActivationState")
        if state == "FactoryActivated":
            self.status_label.set_text("✅ Activation successful!")
        else:
            self.status_label.set_text("❌ Activation failed! Try again.")
            GLib.idle_add(self.activate_button.set_sensitive, True)
        return False

    # ---------------- Backup/Restore ----------------
    def create_backup(self, button):
        os.makedirs(BACKUP_FOLDER, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")
        self.backup_status.set_text(f"Creating backup at {backup_path}...")
        threading.Thread(target=self.backup_task, args=(backup_path,)).start()

    def backup_task(self, path):
        output = self.execute_command("idevicebackup2", "backup", path)
        GLib.idle_add(self.backup_status.set_text, f"Backup completed at {path}.")

    def restore_backup(self, button):
        backups = [f for f in os.listdir(BACKUP_FOLDER) if os.path.isdir(os.path.join(BACKUP_FOLDER, f))]
        if not backups:
            self.backup_status.set_text("No backups available.")
            return
        latest_backup = os.path.join(BACKUP_FOLDER, sorted(backups)[-1])
        self.backup_status.set_text(f"Restoring backup from {latest_backup}...")
        threading.Thread(target=self.restore_task, args=(latest_backup,)).start()

    def restore_task(self, path):
        output = self.execute_command("idevicebackup2", "restore", path)
        GLib.idle_add(self.backup_status.set_text, f"Restore completed from {path}.")

    # ---------------- File Manager ----------------
    def mount_filesystem(self, button):
        os.makedirs(MOUNT_POINT, exist_ok=True)
        self.file_status_label.set_text("Mounting filesystem...")
        threading.Thread(target=self.mount_task).start()

    def mount_task(self):
        self.execute_command("ifuse", MOUNT_POINT)
        GLib.idle_add(self.file_status_label.set_text, f"Mounted at {MOUNT_POINT}")

    def unmount_filesystem(self, button):
        self.file_status_label.set_text("Unmounting filesystem...")
        threading.Thread(target=self.unmount_task).start()

    def unmount_task(self):
        self.execute_command("fusermount", "-u", MOUNT_POINT)
        GLib.idle_add(self.file_status_label.set_text, "Filesystem unmounted.")

    # ---------------- Error ----------------
    def show_error(self, message):
        dialog = Gtk.MessageDialog(parent=self, flags=0,
                                   message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.OK,
                                   text="Error")
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()


# ---------------- Main ----------------
def main():
    win = Linux3uTools()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()

if __name__ == "__main__":
    main()

