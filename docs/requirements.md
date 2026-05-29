# Banking AI-Agent — Yêu cầu dự án (Microservice Architecture)

> **Môn học:** Applications of Natural Language Processing in Industry (CSC15012)
> **Giảng viên:** Dr. Nguyễn Hồng Bửu Long & Dr. Lê Đức Khoan
> **Thời gian:** 04/2026

---

## 1. Tổng quan dự án

Nâng cấp hệ thống AI Agentic Workflow hỗ trợ khách hàng ngân hàng từ phiên bản chạy local (monolith) sang kiến trúc **multi-service deployment**. 
Mục tiêu chính là thiết kế, containerize (đóng gói), và triển khai ứng dụng AI thành một hệ thống phân tán với các service độc lập giao tiếp qua **HTTP** và **gRPC**.

Hệ thống triển khai phải bao gồm:
1. **API Gateway**: Nhận HTTP request từ bên ngoài và điều phối agentic workflow.
2. **Intent Service**: Một gRPC microservice độc lập chịu trách nhiệm nhận diện intent.
3. **Ollama Service**: Phục vụ mô hình sinh ngôn ngữ (response generation).
4. **Frontend**: Giao diện người dùng đơn giản (tùy chọn nhưng cần thiết để test).
5. Các thành phần workflow khác: priority detection, policy retrieval, validation, và routing.

---

## 2. Yêu cầu chức năng

### 2.1 Kiến trúc hệ thống (System Architecture)

- **API Gateway (FastAPI)**: 
  - Là điểm vào (entry point) chính của hệ thống.
  - Nhận tin nhắn khách hàng.
  - Gọi **Intent Service** thông qua **gRPC**.
  - Thực thi các node còn lại trong workflow.
  - Gọi mô hình sinh phản hồi qua **Ollama Service** bằng **HTTP**.
  - Trả về kết quả có cấu trúc.
  - Cung cấp các endpoints:
    - `GET /health`: Kiểm tra trạng thái hệ thống.
    - `GET /config`: Trả về cấu hình hiện tại của hệ thống.
    - `POST /run-agent`: Thực thi toàn bộ agentic workflow.

- **Intent Service (gRPC)**:
  - Microservice độc lập.
  - Cung cấp method gRPC để dự đoán intent (đầu vào: tin nhắn khách hàng; đầu ra: predicted intent, confidence score).
  - Có thể sử dụng fine-tuned model (từ Lab 2) hoặc Ollama để thực hiện dự đoán.
  - Yêu cầu định nghĩa file `.proto` và generate code client/server tương ứng.

- **Ollama Service**:
  - Chạy mô hình ngôn ngữ lớn (LLM), khuyến nghị dùng **gpt-oss:20b**.
  - Xử lý Response Generation node với input gồm: customer message, predicted intent, priority/risk info, retrieved policy content.
  - Output gồm: draft reply, missing info, next recommended action.

### 2.2 Docker Containerization

- Cần viết `Dockerfile` cho các services:
  - API Gateway (Backend)
  - Intent Service
  - Frontend
- Đảm bảo mỗi service có thể chạy độc lập và tái tạo được môi trường.

### 2.3 Multi-container Deployment (Docker Compose)

- Tạo file `docker-compose.yml` để chạy toàn bộ hệ thống.
- Cấu hình ít nhất các services: `api-gateway` (backend), `intent-service`, `frontend`.
- Phải định nghĩa:
  - Service names
  - Exposed ports
  - Environment variables
  - Inter-service dependencies (depends_on)
  - Networks (API Gateway gọi Intent Service qua network nội bộ, API Gateway nhận request từ Frontend qua network khác).

---

## 3. Yêu cầu về deliverables

### 3.1 README.md

README của dự án phải bao gồm:
- Mô tả kiến trúc microservice.
- Hướng dẫn cách generate gRPC code từ file `.proto`.
- Hướng dẫn build Docker images.
- Hướng dẫn chạy hệ thống với Docker Compose.
- Mô tả vai trò của từng container trong hệ thống.

### 3.2 Video demo

- Submit **1 video ngắn** demo hệ thống.
- Video cần thể hiện:
  - Giới thiệu tổng quan hệ thống.
  - Chạy hệ thống bằng lệnh `docker-compose up`.
  - Gọi API Gateway (qua UI hoặc curl).
  - Hiển thị kết quả workflow cuối cùng.
- Thời lượng khuyến nghị: **2–3 phút**.

---

## 4. Cấu trúc source code (khuyến nghị)

```
banking-service/
├── backend/                  # API Gateway
│   ├── app/
│   │   ├── agent/            # Orchestrator
│   │   ├── clients/          # HTTP & gRPC clients
│   │   │   ├── intent_grpc/  # Generated gRPC code
│   │   ├── core/             # Settings & Schemas
│   │   ├── data/             # Policies
│   │   └── nodes/            # Workflow nodes
│   ├── Dockerfile
│   ├── README.md
│   ├── requirements.txt
│   └── run.py
├── frontend/                 # UI
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── intent_service/           # gRPC Microservice
│   ├── app/
│   │   └── ...               # Internal logic
│   ├── Dockerfile
│   ├── intent_service.proto  # Protobuf definition
│   ├── intent_service_pb2.py # Generated code
│   ├── intent_service_pb2_grpc.py
│   ├── Makefile              # Build script cho gRPC
│   ├── requirements.txt
│   └── server.py             # gRPC Server
└── docker-compose.yml        # Orchestration
```

---

## 5. Checklist tổng hợp cần thực hiện

- [x] Tách biệt Intent Detection thành **gRPC service** độc lập.
- [x] Định nghĩa `intent_service.proto` và viết `Makefile` để generate code.
- [x] Implement `Intent Service` (gRPC server) xử lý request và trả về intent + confidence.
- [x] Refactor **API Gateway** (Backend):
  - [x] Thêm endpoint `GET /health`
  - [x] Thêm endpoint `GET /config`
  - [x] Thêm endpoint `POST /run-agent`
  - [x] Gọi Intent Service thông qua gRPC client.
- [x] Viết `Dockerfile` cho Backend, Intent Service, Frontend.
- [x] Viết `docker-compose.yml` định nghĩa các container, ports, environment variables và networks.
- [x] Cập nhật `README.md` với đầy đủ kiến trúc và hướng dẫn.
- [ ] Quay video demo (2-3 phút) chứng minh hệ thống chạy bằng Docker Compose và giao tiếp gRPC thành công.
