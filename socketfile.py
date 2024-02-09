import socket
import threading
import json
from A202.settings import message_queue
from balls.serializers import LocationSerializer, RouteSerializer
from devices.models import Device

Device_List = list(Device.objects.values_list('serial_num', flat=True))
client_sockets = []  
def handle_client(client_sock, client_addr, client_sockets):
    try:
        while True:
            print(message_queue)
            data = client_sock.recv(1024)
            if data == b'exit':
                break
            received_data = data.decode("utf-8")
            print(message_queue.get())
            json_info = json.loads(received_data)
            # print(f'Received from {client_addr}: {received_data}')


            try:
                device_info = json_info["device_info"]
                num_of_frames_info = json_info["num_of_frames"]
            except KeyError:
                continue

            if num_of_frames_info != 1:
                print('경로 좌표')
                if device_info in db:
                    print('저장완료')
                    loca_serializer = LocationSerializer(loca_file=json_info, is_quiz=0)
                    if loca_serializer.is_valid(raise_exception=True):
                        loca_serializer.save()
                        client_sock.sendall('Route success!!'.encode())
                    else:
                        pass
            
            else:
                print('루트 좌표')
                if device_info in db:
                    print('저장완료')
                    client_sock.sendall('Location success!!'.encode())

            

    except Exception as e:
        print(f'Error handling client {client_addr}: {e}')

    finally:
        client_sockets.remove(client_sock)
        client_sock.close()
        print(f'Connection with {client_addr} closed.')


def start_server():
    print(Device_List)
    server_host = '0.0.0.0'
    server_port = 55555

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((server_host, server_port))
    server_sock.listen(5)
    
    print(f'Server is listening on {server_host}:{server_port}')

    try:
        
        send_thread = threading.Thread(target=handle_user_input, args=(client_sockets,))
        send_thread.start()

        connect_thread = threading.Thread(target=wait_for_clients, args=(server_sock, client_sockets ))
        connect_thread.start()
 



    except KeyboardInterrupt:
        print('Server is shutting down...')
        server_sock.close()

def handle_user_input(client_sockets):
   
    while True:
        message = message_queue.get()
        # message = input()
        print(client_sockets)
        if message.lower() == 'exit':
            break
        target_client_index = int(message[0])
        if 0 <= target_client_index < len(client_sockets):
            target_client_socket = client_sockets[target_client_index]
            target_client_socket.sendall(message[1:].encode('utf-8'))
        else:
            print(f'Invalid client index: {target_client_index}')


def wait_for_clients(server_sock, client_sockets):
    print('시작')
    while True:
        client_sock, client_addr = server_sock.accept()
        print(f'Accepted connection from {client_addr}')
        client_sockets.append(client_sock)
        # print(client_sockets)
        new_client_thread = threading.Thread(target=handle_client, args=(client_sock, client_addr, client_sockets))
        new_client_thread.start()
