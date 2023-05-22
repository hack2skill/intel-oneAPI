from fastapi import APIRouter
import os
import re
import chardet
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearnex import patch_sklearn
patch_sklearn()
from sklearn.cluster import KMeans

# Create an instance of APIRouter
router = APIRouter()

@router.get("/api1")
def api1_handler():
    # Add your logic here
    return {"message": "This is API 1"}

@router.post("/api1")
def api1_post_handler():
    # Add your logic here
    return {"message": "POST request received on API 1"}
