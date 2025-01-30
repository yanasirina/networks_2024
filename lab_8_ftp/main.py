import os
import json
import shutil
import socketserver

WORKING_DIR = "./server_files"  # Рабочая директория
os.makedirs(WORKING_DIR, exist_ok=True)


class FileManagerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(1024).decode("utf-8")
            if not data:
                break

            try:
                request = json.loads(data)
                command = request.get("command")

                if command == "list":
                    response = self.list_files()
                elif command == "mkdir":
                    response = self.make_directory(request.get("name"))
                elif command == "rmdir":
                    response = self.remove_directory(request.get("name"))
                elif command == "create":
                    response = self.create_file(request.get("name"), request.get("content"))
                elif command == "copy":
                    response = self.copy_file(request.get("src"), request.get("dst"))
                elif command == "rename":
                    response = self.rename_file(request.get("old"), request.get("new"))
                elif command == "delete":
                    response = self.delete_file(request.get("name"))
                elif command == "read":
                    response = self.read_file(request.get("name"))
                else:
                    response = {"status": "error", "message": "bad command"}

            except json.JSONDecodeError:
                response = {"status": "error", "message": "Invalid JSON format"}

            self.request.sendall(json.dumps(response).encode("utf-8"))

    def list_files(self):
        try:
            files = os.listdir(WORKING_DIR)
            return {"status": "success", "files": files}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def make_directory(self, name):
        if not name:
            return {"status": "error", "message": "No directory name provided"}
        try:
            os.makedirs(os.path.join(WORKING_DIR, name), exist_ok=True)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def remove_directory(self, name):
        if not name:
            return {"status": "error", "message": "No directory name provided"}
        try:
            shutil.rmtree(os.path.join(WORKING_DIR, name))
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def create_file(self, name, content):
        if not name:
            return {"status": "error", "message": "No file name provided"}
        try:
            with open(os.path.join(WORKING_DIR, name), "w") as f:
                f.write(content or "")
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def copy_file(self, src, dst):
        if not src or not dst:
            return {"status": "error", "message": "Source or destination missing"}
        try:
            shutil.copy(os.path.join(WORKING_DIR, src), os.path.join(WORKING_DIR, dst))
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def rename_file(self, old, new):
        if not old or not new:
            return {"status": "error", "message": "Old or new file name missing"}
        try:
            os.rename(os.path.join(WORKING_DIR, old), os.path.join(WORKING_DIR, new))
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_file(self, name):
        if not name:
            return {"status": "error", "message": "No file name provided"}
        try:
            os.remove(os.path.join(WORKING_DIR, name))
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def read_file(self, name):
        if not name:
            return {"status": "error", "message": "No file name provided"}
        try:
            with open(os.path.join(WORKING_DIR, name), "r") as f:
                content = f.read()
            return {"status": "success", "content": content}
        except Exception as e:
            return {"status": "error", "message": str(e)}


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
    with ThreadedTCPServer((HOST, PORT), FileManagerHandler) as server:
        print(f"Server started on {HOST}:{PORT}")
        server.serve_forever()
