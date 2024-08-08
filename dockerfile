# Use the blang/latex image as the base image
FROM blang/latex:ubuntu

# Install pip
RUN apt-get update && \
    apt-get install -y python3-pip

# Install Python packages
RUN pip3 install pylatex

# Set the working directory
WORKDIR /usr/src/app

# Copy the application code
COPY . .

# Set the entry point for the container
CMD ["python3", "your_script.py"]



































# # Use an official Ubuntu base image
# FROM ubuntu:22.04

# # Set the DEBIAN_FRONTEND to noninteractive to avoid prompts during package installation
# ENV DEBIAN_FRONTEND=noninteractive

# # Install necessary dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     wget \
#     lsb-release \
#     software-properties-common \
#     ca-certificates \
#     gnupg \
#     dirmngr \
#     python3 \
#     python3-pip

# # Add the MiKTeX repository and key
# RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889 \
#     echo "deb http://miktex.org/download/ubuntu bionic universe" | tee /etc/apt/sources.list.d/miktex.list

# # Update package lists and install MiKTeX
# # RUN apt-get install miktex 

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip3 install --no-cache-dir -r requirements.txt

# # Expose the port the app runs on
# EXPOSE 5000

# # Run the application
# CMD ["python3", "app.py"]


#using miktex



# # Use a base image that includes MiKTeX
# FROM miktex/miktex

# # Install Python and other dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     python3 
#     # python3-pip 
#     # && rm -rf /var/lib/apt/lists/*

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed Python packages specified in requirements.txt
# RUN pip3 install --no-cache-dir -r requirements.txt

# # Expose the port the app runs on
# EXPOSE 5000

# # Run the application
# CMD ["python3", "app.py"]
