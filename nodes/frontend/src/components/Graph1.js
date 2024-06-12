import React, { Component } from 'react';
import CanvasJSReact from '@canvasjs/react-charts';
import axios from 'axios';

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

class Graph1 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            unemploymentDataPoints: [],
            populationDataPoints: [],
            userRole: null
        };
    }

    componentDidMount() {
        this.fetchData();
        this.fetchUserRole();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.selectedCountry !== this.props.selectedCountry || prevProps.yearRange !== this.props.yearRange) {
            this.fetchData();
        }
    }

    fetchData = async () => {
        await this.fetchUnemploymentData();
        await this.fetchPopulationData();
    };

    fetchUserRole = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`http://127.0.0.1:8001/roles`, {
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            const roles = response.data.roles.map(role => role.name);
            this.setState({ userRole: roles.includes('export') ? 'export' : 'user' });
        } catch (error) {
            console.error('Error fetching user role', error);
        }
    };

    fetchUnemploymentData = async () => {
        const { selectedCountry, yearRange } = this.props;
        if (!selectedCountry) return;

        const currentYear = new Date().getFullYear();
        const yearStart = currentYear - yearRange + 1;
        const yearEnd = currentYear;

        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`http://127.0.0.1:8001/api/unemployment`, {
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                params: {
                    code: selectedCountry,
                    year_start: yearStart,
                    year_end: yearEnd
                }
            });

            const unemploymentData = response.data.values.map(data => ({
                x: new Date(data.year, 0),
                y: parseFloat(data.value)
            }));

            this.setState({ unemploymentDataPoints: unemploymentData });
        } catch (error) {
            console.error('Error fetching unemployment data', error);
        }
    };

    fetchPopulationData = async () => {
        const { selectedCountry, yearRange } = this.props;
        if (!selectedCountry) return;

        const currentYear = new Date().getFullYear();
        const yearStart = currentYear - yearRange + 1;
        const yearEnd = currentYear;

        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`http://127.0.0.1:8001/api/population`, {
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                params: {
                    code: selectedCountry,
                    year_start: yearStart,
                    year_end: yearEnd
                }
            });

            const populationData = response.data.values.map(data => ({
                x: new Date(data.year, 0),
                y: parseInt(data.value, 10)
            }));

            this.setState({ populationDataPoints: populationData });
        } catch (error) {
            console.error('Error fetching population data', error);
        }
    };

    downloadDataAsJson = (dataPoints, fileName) => {
        const blob = new Blob([JSON.stringify(dataPoints, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        a.click();
        URL.revokeObjectURL(url);
    };

    render() {
        const { unemploymentDataPoints, populationDataPoints, userRole } = this.state;

        const options1 = {
            title: {
                text: "Unemployment Rate"
            },
            axisX: {
                title: "Year",
                valueFormatString: "YYYY"
            },
            axisY: {
                title: "Unemployment Rate (%)"
            },
            data: [{
                type: "line",
                dataPoints: unemploymentDataPoints
            }]
        };

        const options2 = {
            title: {
                text: "Population"
            },
            axisX: {
                title: "Year",
                valueFormatString: "YYYY"
            },
            axisY: {
                title: "Population"
            },
            data: [{
                type: "line",
                dataPoints: populationDataPoints
            }]
        };

        return (
            <div>
                <div className='container'>
                    {userRole === 'export' && (
                        <button 
                            onClick={() => this.downloadDataAsJson(unemploymentDataPoints, 'unemployment_data.json')}
                            style={{ marginBottom: '20px' }}
                        >
                            Download Unemployment Data as JSON
                        </button>
                    )}
                    <CanvasJSChart options={options1} />
                </div>
                <div className='container'>
                    {userRole === 'export' && (
                        <button 
                            onClick={() => this.downloadDataAsJson(populationDataPoints, 'population_data.json')}
                            style={{ marginBottom: '20px' }}
                        >
                            Download Population Data as JSON
                        </button>
                    )}
                    <CanvasJSChart options={options2} />
                </div>
            </div>
        );
    }
}

export default Graph1;
