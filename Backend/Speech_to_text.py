from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
from google.cloud import speech_v1p1beta1 as speech
import os
