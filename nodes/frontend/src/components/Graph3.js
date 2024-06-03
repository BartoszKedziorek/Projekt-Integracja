import React, { useState } from 'react';
import CanvasJSReact from '@canvasjs/react-charts';

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

const Graph3 = () => {
    const [filter, setFilter] = useState('top');
    const [yearRange, setYearRange] = useState(10);

    const allData = {
        women: [
            { label: "Health & Clinical Science", y: 85 },
            { label: "Education", y: 79 },
            { label: "Psychology", y: 77 },
            { label: "Language & Literature", y: 68 },
            { label: "Communication Tech", y: 63 },
            { label: "Art", y: 61 },
            { label: "Biomedical Science", y: 59 },
            { label: "Social Science & History", y: 49 },
            { label: "Business", y: 49 },
            { label: "Computer & Info Science", y: 18 }
        ],
        men: [
            { label: "Health & Clinical Science", y: 15 },
            { label: "Education", y: 21 },
            { label: "Psychology", y: 23 },
            { label: "Language & Literature", y: 32 },
            { label: "Communication Tech", y: 37 },
            { label: "Art", y: 39 },
            { label: "Biomedical Science", y: 41 },
            { label: "Social Science & History", y: 51 },
            { label: "Business", y: 51 },
            { label: "Computer & Info Science", y: 82 }
        ]
    };

    const getFilteredData = (data) => {
        let filteredData = [...data];

        if (filter === 'top') {
            filteredData.sort((a, b) => b.y - a.y);
        } else {
            filteredData.sort((a, b) => a.y - b.y);
        }

        return filteredData.slice(0, yearRange);
    };

    const options = {
        title: {
            text: "Popular Majors Opted by Women & Men"
        },
        toolTip: {
            shared: true
        },
        legend: {
            verticalAlign: "top"
        },
        axisY: {
            suffix: "%"
        },
        data: [
            {
                type: "stackedBar100",
                color: "#9bbb59",
                name: "Women",
                showInLegend: true,
                indexLabel: "{y}",
                indexLabelFontColor: "white",
                yValueFormatString: "#,###'%'",
                dataPoints: getFilteredData(allData.women)
            },
            {
                type: "stackedBar100",
                color: "#7f7f7f",
                name: "Men",
                showInLegend: true,
                indexLabel: "{y}%",
                indexLabelFontColor: "white",
                yValueFormatString: "#,###'%'",
                dataPoints: getFilteredData(allData.men)
            }
        ]
    };

    return (
        <div>
            <div className="filters">
                <label>
                    Filtr:
                    <select value={filter} onChange={(e) => setFilter(e.target.value)}>
                        <option value="top">MAX</option>
                        <option value="bottom">MIN</option>
                    </select>
                </label>
                <label>
                    Przedział lat:
                    <select value={yearRange} onChange={(e) => setYearRange(parseInt(e.target.value, 10))}>
                        <option value={10}>10</option>
                        <option value={15}>15</option>
                        <option value={20}>20</option>
                        <option value={25}>25</option>
                    </select>
                </label>
            </div>
            <div className='container'>
                <CanvasJSChart options={options} />
                <CanvasJSChart options={options} />
                <CanvasJSChart options={options} />
            </div>
        </div>
    );
};

export default Graph3;
