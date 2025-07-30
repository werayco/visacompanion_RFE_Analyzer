# How to run the VisaCompanion RFE Analyzer (Using Docker)

- Clone this repo:
```console
git clone https://github.com/werayco/visacompanion_RFE_Analyzer.git

```
- Navigate to the working directory

```console
cd visacompanion_RFE_Analyzer
```
- Add your Claude API key and Agent Temperature in your .env file

```console
CLAUDE_API_KEY = 
AGENT_TEMP = 
```
- After navigating to the working directory, execute this command below in your CLI to build a custom docker image from the dockerfile.


```console
docker build -t visacom:latest .

```
- After the image, run the container using this command.

```console
docker run -p 8080:8080 visacom:latest
```
- Open any API CLient of your choice (POSTMAN preferably) and send a GET request to test if the server is actually active

```console
GET http://127.0.0.1:8080
```
- The response of the GET request above is:

```json
{"status": "successful", "response": "You are welcome to the server!"}
```
- Now for the main work, send a POST request to this endpoint, having a key of 'file' and the value should be the EB-1A petition you want to analyze.
```console
POST http://127.0.0.1:8080/upload
```
- Below is the response of that post request:

![alt text](screenshots/image-1.png)

- After response is received, Click the "Save Response" button (top right of response panel).

- Select "Save to a file", and the Analysis Word Document will be downloaded to your machine.
