import argparse
from HomeveeCloud import HomeveeCloud


def main():
    parser = argparse.ArgumentParser(description='Homevee-Cloud for Servers')
    parser.add_argument('--domain', required=True, type=str, help='Domain that the server is reachable under (z.B. free.cloud.homevee.de)')
    parser.add_argument('--port', default=7778, type=int, help='The Port the Homevee-Server should listen on')
    parser.add_argument('--server_secret', required=True, type=str, help='The secret for communication with the main server')
    parser.add_argument('--max_clients', default=50, type=int, help='Number of clients simultaneously')
    parser.add_argument('--buffer_size', default=64, type=int, help='Buffer size for client communication')
    parser.add_argument('--debug', default=False, type=bool, help='Is the server in debug mode?')
    args = parser.parse_args()

    homevee_cloud = HomeveeCloud(args.server_secret, args.domain, args.port, args.max_clients, args.debug, args.buffer_size)
    homevee_cloud.start_server()

if __name__ == "__main__":
    main()