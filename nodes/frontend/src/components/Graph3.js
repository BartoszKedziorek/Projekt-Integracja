import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CanvasJSReact from '@canvasjs/react-charts';

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

const Graph3 = ({ extreme_type, years }) => {
    const [populationData, setPopulationData] = useState([]);

    useEffect(() => {
        const fetchPopulationData = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get('http://127.0.0.1:8001/api/population/extreme', {
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    },
                    params: {
                        amount: 10,
                        extreme_type: extreme_type,
                        years: years
                    }
                });

                if (response.data && response.data.length > 0) {
                    const data = response.data;

                    const populationPoints = data.map(item => ({
                        label: item.code,
                        y: parseFloat(item.value)
                    }));

                    setPopulationData(populationPoints);
                    
                } else {
                    setPopulationData([]);
                }
            } catch (error) {
                console.error('Error fetching population data', error);
            }
        };
        fetchPopulationData();
    }, [extreme_type, years]);

    const options = {
        animationEnabled: true,
        title: {
            text: `Top ${years} Countries by Population (${extreme_type === 'max' ? 'Highest' : 'Lowest'})`
        },
        axisX: {
            title: "Country",
            reversed: true,
        },
        axisY: {
            title: "Population",
            interval: 1,
            labelPlacement: "inside",
            tickPlacement: "inside"
        },
        data: [{
            type: "column",
            dataPoints: populationData
        }]
    };

    return (
        <div className='chart-container'>
            <CanvasJSChart options={options} />
        </div>
    );
};

export default Graph3;
