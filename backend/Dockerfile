FROM python:3.13
WORKDIR /fastapi-onion-template
COPY backend /fastapi-onion-template/backend/
COPY app.conf /fastapi-onion-template/
RUN pip install --no-cache-dir --upgrade -r /fastapi-onion-template/backend/requirements.txt
RUN touch /var/log/fastapi-onion-template.log
RUN cd backend && ls && alembic upgrade head && cd ..