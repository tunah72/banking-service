GRPC_SOURCES = intent_service_pb2.py intent_service_pb2_grpc.py

all: $(GRPC_SOURCES)

$(GRPC_SOURCES): intent_service.proto
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. intent_service.proto

clean:
	rm -f $(GRPC_SOURCES)
