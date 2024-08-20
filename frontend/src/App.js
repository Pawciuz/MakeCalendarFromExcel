import React from 'react';
import FileUpload from "./components/FileUpload";
import SampleTable from "./components/SampleTable";

const App = () => {
    return (
        <div className="container">
            <h1>Prześlij plik Excel i wygeneruj kalendarz</h1>
            <FileUpload />
            <h2>Przykładowy plik Excel</h2>
            <SampleTable />
        </div>
    );
};


export default App;
