
import sys

# 1. Add the directory THAT CONTAINS the 'stock' folder to sys.path
sys.path.insert(0, r"C:\Users\moham\Desktop\dev\webstock")

import grpc
from stock import stock_pb2 as stock_pb2
from stock import stock_pb2_grpc as stock_pb2_grpc

def generate_updates():
    updates = [
        stock_pb2.StockItemUpdate(item_id="Monitor", quantity=10, operation=stock_pb2.OperationType.ADD),
        stock_pb2.StockItemUpdate(item_id="Scanner", quantity=15, operation=stock_pb2.OperationType.ADD),
        stock_pb2.StockItemUpdate(item_id="Laptop", quantity=20, operation=stock_pb2.OperationType.ADD),
        stock_pb2.StockItemUpdate(item_id="Desktop", quantity=20, operation=stock_pb2.OperationType.SUBTRACT),
        stock_pb2.StockItemUpdate(item_id="Printer", quantity=20, operation=stock_pb2.OperationType.SUBTRACT),
    ]
    for update in updates:
        yield update

def run():
    with grpc.insecure_channel('localhost:30051') as channel:
        stub = stock_pb2_grpc.StockServiceStub(channel)
        response = stub.BulkUpdateStock(generate_updates())
        print("Server response: " + str(response.message) + "Processed: " + str(response.items_processed))

if __name__ == '__main__':
    run()