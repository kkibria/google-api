# Google services

## setup

setup virtual environment with,
```
python -m venv .venv
```

install all the dependencies
```
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
pip install --upgrade google-api-python-client
pip install --upgrade google-cloud-texttospeech
```

or just run

```
pip install -r requirements.txt
```


## api key

Download client API keys from google console as `.secrets/client_secret.json`



## Upload to you tube
AI generated videos can be uploaded to youtube using this card from colab.

## text to speech
run `txt2spc.py`


### available voices

<https://cloud.google.com/text-to-speech/docs/voices>

| Language     | Voice type | Voice name      | SSML Gender
| -------------|------------|-----------------|------------
| English (US) | WaveNet    | en-US-Wavenet-A | MALE	
| English (US) | WaveNet    | en-US-Wavenet-B | MALE	
| English (US) | WaveNet    | en-US-Wavenet-C | FEMALE	
| English (US) | WaveNet    | en-US-Wavenet-D | MALE	
| English (US) | WaveNet    | en-US-Wavenet-E | FEMALE	
| English (US) | WaveNet    | en-US-Wavenet-F | FEMALE	
| English (US) | WaveNet    | en-US-Wavenet-G | FEMALE	
| English (US) | WaveNet    | en-US-Wavenet-H | FEMALE	
| English (US) | WaveNet    | en-US-Wavenet-I | MALE	
| English (US) | WaveNet    | en-US-Wavenet-J | MALE  

## speech shaping

<https://cloud.google.com/text-to-speech/docs/ssml>