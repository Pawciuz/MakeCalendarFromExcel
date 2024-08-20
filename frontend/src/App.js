import React from 'react';
import FileUpload from "./components/FileUpload";
import SampleTable from "./components/SampleTable";
import { ToastContainer } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

const App = () => {
    return (
        <>
            <div className="container">
                <h1>Prześlij plik Excel i wygeneruj kalendarz</h1>
                <FileUpload/>
                <h2>Przykładowy plik Excel</h2>
                <SampleTable/>
            </div>
            <ToastContainer
                position="bottom-center"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
                style={{
                    width: '400px',
                    fontSize: '14px',
                }}
            />
        </>
    );
};

export default App;