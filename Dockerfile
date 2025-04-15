# Step 1: Choose a Base Image
FROM python:3.10-slim

# Step 2: Install System Dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set the Working Directory
WORKDIR /app

# Step 4: Copy Requirements File
COPY requirements.txt .

# Step 5: Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy Application Code
COPY . .

# Add this line to ensure the .env file is included
COPY .env /app/.env

# Step 7: Expose the Port
EXPOSE 7860

# Step 8: Define the Command to Run the App
CMD ["python", "app.py"]