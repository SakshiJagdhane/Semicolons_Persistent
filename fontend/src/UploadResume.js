import React, { useState } from "react";
import axios from "axios";

const UploadResume = () => {
    const [file, setFile] = useState(null);
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please select a file first!");
            return;
        }

        setLoading(true);
        const formData = new FormData();
        formData.append("resume", file);

        try {
            const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            setResponse(res.data);
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("Upload failed. Please try again.");
        }
        setLoading(false);
    };

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
            <h2>Resume Keyword Extractor</h2>
            <input type="file" accept="application/pdf" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={loading}>
                {loading ? "Uploading..." : "Upload Resume"}
            </button>

            {response && (
                <div style={{ marginTop: "20px", textAlign: "left", maxWidth: "600px", margin: "auto" }}>
                    <h3>Extracted Text:</h3>
                    <p>{response.resume_text}</p>

                    <h3>Extracted Information:</h3>
                    <pre>{JSON.stringify(response.resume_info, null, 2)}</pre>

                    <h3>Generated Questions:</h3>
                    <ul>
                        {response.questions.map((q, index) => (
                            <li key={index}>{q}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default UploadResume;
