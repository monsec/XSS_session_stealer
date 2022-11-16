FROM node:18.12.1-alpine3.16 AS build
WORKDIR /frontend
COPY frontend .
RUN npm install --production
RUN npm run build

FROM python:3.10.8-alpine3.16
WORKDIR /backend
COPY backend .
RUN pip install -r requirements.txt
COPY --from=build /frontend/build /frontend
EXPOSE 9000 9001
CMD python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 9000 & python -m http.server -d /frontend 9001