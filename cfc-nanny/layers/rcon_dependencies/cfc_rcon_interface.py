import os
import valve.rcon

class RCONInterface:
    def __init__(self):
        self.set_rcon_credentials()

    def set_rcon_credentials(self):
        self.address = os.getenv("RCON_IP")
        self.port = os.getenv("RCON_PORT")
        self.password = os.getenv("RCON_PASSWORD")

        print("Initialized RCON Interface with the following values:")
        print(f"Address: {self.address}")
        print(f"Port: {self.port}")
        print(f"Password: {self.password}")

    def issue_command(self, command):
        connection_address = (self.address, int(self.port))

        try:
            with valve.rcon.RCON(connection_address, self.password, timeout=5) as rcon:
                response = rcon(command)
                print("Rcon response:")
                print(response)

                if response:
                    return True, response

        except valve.rcon.RCONCommunicationError as socket_err:
            print(f"Hit a communication error when trying to issue: '{command}' to '{self.address}:{self.port}'")
            print(socket_err)

            return False, socket_err

        except valve.rcon.RCONTimeoutError as timeout_err:
            print(f"Hit a timeout error when trying to issue: '{command}' to '{self.address}:{self.port}'")
            print(timeout_err)

            return False, timeout_err

        except Exception as generic_err:
            print(f"Hit an unknown error when trying to issue: '{command}' to '{self.address}:{self.port}'")

            return False, generic_err

        print("No conditions met, assuming failure?")
        return False
