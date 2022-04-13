import './DropZone.css';
import React, { useCallback, useState } from 'react'
import axios from 'axios';
import { useDropzone } from 'react-dropzone'
import { Form } from 'react-final-form'
import { host_ip } from '../../../network/api';

let file
export function FileDropzone() {

    const [uploadedFileNames, changeUploadedFileNames] = useState("")

    const onDrop = useCallback(async acceptedFiles => {
        //post selected file
        file = acceptedFiles;
        if (file[0]) {

            let formData = new FormData();
            formData.append("file", file[0]);

            //upload and get filename info in the DB
            const response = await axios.post(host_ip + "graph/upload", formData);
            const filename = response.data
            changeUploadedFileNames(uploadedFileNames =>
                <>
                    {uploadedFileNames}
                    <h5>{filename}</h5>
                </>
            )
        }
    }, [])
    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop })

    return (
        <>
            <div class="dropzone" {...getRootProps()}>
                <input {...getInputProps()} />
                {
                    isDragActive ?
                        <p>Drop the files here ...</p> :
                        <p>Upload File (Drag & Drop)</p>
                }

            </div>

            <h3>Recently upload file info</h3>
            <h3>{uploadedFileNames}</h3>
        </>
    )
}

export function FileForm() {
    const handleSubmit = async (s) => {

    }

    //const { uploadedFileNames, changeUploadedFileNames } = useContext(FileNameContext);

    return (
        <>
            <Form
                onSubmit={handleSubmit}
                render={({ handleSubmit }) => (
                    <form onSubmit={handleSubmit}>
                        <FileDropzone />
                    </form>
                )}
            />
        </>

    )
}