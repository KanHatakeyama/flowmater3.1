from django.shortcuts import render

# Create your views here.
import base64
import io
from rdkit import Chem
from rdkit.Chem import Draw
from django.utils.html import mark_safe
from django.http import HttpResponse
import numpy as np
from PIL import Image, ImageChops

# generate molecule image (as string) from smiles string


def smiles(request, smiles):
    return smiles_to_buffer_img(smiles)


def smiles_to_buffer_img(sm: str, size: int = None) -> str:
    mol = Chem.MolFromSmiles(sm)

    if size is None:
        img = Draw.MolToImage(mol)
    else:
        img = Draw.MolToImage(mol, size=(size, size))

    img = crop_image(img)
    response = HttpResponse(content_type="image/png")
    img.save(response, "png")
    return response


def crop_image(img):
    w, h = img.size
    box = (w*0.01, h*0.01, w*0.99, h*0.99)
    img = img.crop(box)

    # background
    bg = Image.new("RGB", img.size, img.getpixel((0, 0)))

    diff = ImageChops.difference(img, bg)

    # calc boundary
    croprange = diff.convert("RGB").getbbox()
    crop_img = img.crop(croprange)
    return crop_img
