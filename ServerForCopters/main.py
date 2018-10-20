from Server import Server

if __name__ == "__main__":
    server = Server()
    server.accept()
    server.start()
    server.wait_end()
    server.close()

