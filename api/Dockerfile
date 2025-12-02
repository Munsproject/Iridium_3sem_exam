FROM python:3.11-slim

# Arbejdsmappen i containeren
WORKDIR /app

# Kopiér requirements først (bedre caching)
COPY requirements.txt .

# Installer dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Kopiér resten af appen ind i containeren
COPY . .

# Flask kører på port 5000
EXPOSE 5000

# Start Flask
CMD ["python", "app.py"]

