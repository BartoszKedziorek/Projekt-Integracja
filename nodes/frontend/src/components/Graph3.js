import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CanvasJSReact from '@canvasjs/react-charts';

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

const Rankings = () => {
    const [filter, setFilter] = useState('top');
    const [yearRange, setYearRange] = useState(10);
    const [countryData, setCountryData] = useState([]);
    const [unemploymentData, setUnemploymentData] = useState([]);
    const [populationData, setPopulationData] = useState([]);
    const [internetData, setInternetData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8001/api/country');
                setCountryData(response.data);
            } catch (error) {
                console.error('Error fetching country data', error);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        const fetchUnemploymentData = async () => {
            try {
                const promises = countryData.map(country => axios.get(`http://127.0.0.1:8001/api/unemployment?code=${country.code}&year_end=${yearRange}&year_start=${yearRange - 9}`));
                const responses = await Promise.all(promises);
                const data = responses.map(response => response.data.values);
                setUnemploymentData(data);
            } catch (error) {
                console.error('Error fetching unemployment data', error);
            }
        };

        if (countryData.length > 0) {
            fetchUnemploymentData();
        }
    }, [countryData, yearRange]);

    useEffect(() => {
        const fetchPopulationData = async () => {
            try {
                const promises = countryData.map(country => axios.get(`http://127.0.0.1:8001/api/population?code=${country.code}&year_end=${yearRange}&year_start=${yearRange - 9}`));
                const responses = await Promise.all(promises);
                const data = responses.map(response => response.data.values);
                setPopulationData(data);
            } catch (error) {
                console.error('Error fetching population data', error);
            }
        };

        if (countryData.length > 0) {
            fetchPopulationData();
        }
    }, [countryData, yearRange]);

    useEffect(() => {
        const fetchInternetData = async () => {
            try {
                const promises = countryData.map(country => axios.get(`http://127.0.0.1:8001/api/internet?code=${country.code}&year_end=${yearRange}&year_start=${yearRange - 9}`));
                const responses = await Promise.all(promises);
                const data = responses.map(response => response.data.values);
                setInternetData(data);
            } catch (error) {
                console.error('Error fetching internet data', error);
            }
        };

        if (countryData.length > 0) {
            fetchInternetData();
        }
    }, [countryData, yearRange]);

    const getFilteredData = (data) => {
        let filteredData = [...data];

        if (filter === 'top') {
            filteredData.sort((a, b) => b.value - a.value);
        } else {
            filteredData.sort((a, b) => a.value - b.value);
        }

        return filteredData.slice(0, 10); // only top 10 for simplicity
    };

    const renderChart = (dataPoints, title) => {
        const options = {
            title: {
                text: title
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
                    name: "Data 1",
                    showInLegend: true,
                    indexLabel: "{y}",
                    indexLabelFontColor: "red",
                    yValueFormatString: "#,###'%'",
                    dataPoints: getFilteredData(dataPoints)
                }
            ]
        };

        return <CanvasJSChart options={options} />;
    };

    const handleChangeFilter = (e) => {
        setFilter(e.target.value);
    };

    const handleChangeYearRange = (e) => {
        setYearRange(parseInt(e.target.value, 10));
    };

    return (
        <div>
            <div className="filters">
                <label>
                    Filter:
                    <select value={filter} onChange={handleChangeFilter}>
                        <option value="top">Top</option>
                        <option value="bottom">Bottom</option>
                    </select>
                </label>
                <label>
                    Year Range:
                    <select value={yearRange} onChange={handleChangeYearRange}>
                        <option value={5}>5</option>
                        <option value={10}>10</option>
                        <option value={15}>15</option>
                        <option value={20}>20</option>
                    </select>
                </label>
            </div>
            <div className='container'>
                <div>
                    {renderChart(unemploymentData, 'Unemployment Rate')}
                </div>
                <div>
                    {renderChart(populationData, 'Population')}
                </div>
                <div>
                    {renderChart(internetData, 'Internet Access')}
                </div>
            </div>
        </div>
    );
};

export default Rankings;
