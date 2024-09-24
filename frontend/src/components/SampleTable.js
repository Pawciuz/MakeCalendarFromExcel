import React from 'react';

const SampleTable = () => {
    return (
        <table>
            <thead>
            <tr>
                <th>Data</th>
                <th>Godzina rozpoczecia</th>
                <th>Godzina zakonczenia</th>
                <th>Nazwa wydarzenia</th>
                <th>Powtarzaj (optional)</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>2024-08-01</td>
                <td>10:00:00</td>
                <td>17:00:00</td>
                <td>Spotkanie z zespołem</td>
                <td>tydzień</td>
            </tr>
            <tr>
                <td>2024-08-02</td>
                <td>12:00:00</td>
                <td>13:00:00</td>
                <td>Lunch z klientem</td>
                <td>2 tydzień</td>
                </tr>
            <tr>
                <td>2024-08-03</td>
                <td>09:00:00</td>
                <td>11:00:00</td>
                <td>Prezentacja projektu</td>
                <td>miesiąc</td>
            </tr>
            </tbody>
        </table>
    );
};

export default SampleTable;
