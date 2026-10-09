import sys

# 1. Add the directory THAT CONTAINS the 'stock' folder to sys.path
sys.path.insert(0, r"C:\Users\moham\Desktop\dev\webstock")

import os
import django

# 1. Point to your Django project's settings module
# (Replace 'myproject' with your actual Django project directory name)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstock.settings')

# 2. Setup Django
django.setup()


import concurrent.futures
import grpc
from django.db import transaction
from stock import stock_pb2
from stock import stock_pb2_grpc
from stock_operations.models import Device
from django.dispatch import Signal
from django.contrib.auth.models import User
from audit.models import StockAuditLog
from django.contrib.contenttypes.models import ContentType
from django import db
from strategy.save_records import *

#python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. your_file.proto

class StockServicer(stock_pb2_grpc.StockServiceServicer):

    def BulkUpdateStock(self, request_iterator, context):
        change = 0
        count = 0
        prev_qty = 0
        new_qty = 0
        try:
            #with transaction.atomic():
            for update in request_iterator:

                # Retrieve the item using Django ORM select_for_update to lock the row
                item = Device.objects.select_for_update().get(name=update.item_id)

                #item._previous_quantity = item.stock_number

                if update.operation == stock_pb2.OperationType.ADD:
                    prev_qty = item.stock_number
                    item.stock_number += update.quantity
                    _action = "Addition"
                    change = update.quantity
                    new_qty = prev_qty + change
                elif update.operation == stock_pb2.OperationType.SUBTRACT:

                    if item.stock_number < update.quantity:
                        context.abort(
                            grpc.StatusCode.FAILED_PRECONDITION,
                            f"Insufficient stock for item {item.name}"
                        )
                    prev_qty = item.stock_number
                    item.stock_number -= update.quantity
                    _action = "Subtraction"
                    change = - update.quantity
                    new_qty = prev_qty + change
                else:
                    _action = "UNKNOWN"

                item.save()
                count += 1

                #StockAuditLog.objects.create(
                #    user=User.objects.get(username="grpc_client"),
                #    content_type=ContentType.objects.get_for_model(item),
                #    object_id=item.pk,
                    # object_repr=str(instance),
                #    object_repr=item.name,
                #    action= "Addition" if change >=0 else "Subtraction",
                #    quantity_change=change,
                #    previous_quantity=prev_qty,
                #    new_quantity=new_qty,
                    # reason=getattr(instance, '_change_reason', 'Standard update')
                #)
                context = ContextSaving(SaveGrpcRecords(item=item,
                                                        action=_action,
                                                        change=change,
                                                        count=0,
                                                        prev_qty=prev_qty,
                                                        new_qty=new_qty))
                context.record()

                #self.grpc_user_processed.send(sender=Device)

            return stock_pb2.BulkUpdateResponse(
                success=True,
                items_processed=count,
                message=f"Successfully processed {count} items."
            )

        except Device.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "One or more items were not found.")
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

        finally:
            # Crucial for multi-threaded gRPC servers running Django ORM
            db.connections.close_all()




def serve():
    # 2. Instantiate a gRPC server with a thread pool to handle concurrent requests
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))

    # 3. Register your servicer class with the server instance
    stock_pb2_grpc.add_StockServiceServicer_to_server(StockServicer(), server)

    # 4. Bind the server to an IP address and port
    # '0.0.0.0' listens on all local network interfaces (IPv4)
    # '[::]' listens on both IPv4 and IPv6
    port = "30051"
    server.add_insecure_port(f"0.0.0.0:{port}")

    # 5. Start the server
    server.start()
    print(f"gRPC Server running on port {port}...")

    # 6. Keep the main thread alive so the server runs continuously
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nStopping gRPC Server...")
        server.stop(0)


if __name__ == "__main__":
    serve()