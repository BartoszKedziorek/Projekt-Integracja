import React, { Component } from 'react';
import CanvasJSReact from '@canvasjs/react-charts';
import axios from 'axios';

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

class Graph1 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            unemploymentDataPoints: [],
            populationDataPoints: []
        };
    }

    componentDidMount() {
        this.fetchData();
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

    fetchUnemploymentData = async () => {
    const { selectedCountry, yearRange } = this.props;
    if (!selectedCountry) return;

    const currentYear = 2022;
    const yearStart = currentYear - yearRange + 1;
    const yearEnd = currentYear;

    try {
        const response = await axios.get(`http://127.0.0.1:8001/api/unemployment?code=${selectedCountry}&year_end=${yearEnd}&year_start=${yearStart}`, {
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

        const currentYear = 2022;
        const yearStart = currentYear - yearRange + 1;
        const yearEnd = currentYear;

        try {
            const response = await axios.get(`http://127.0.0.1:8001/api/population?code=${selectedCountry}&year_end=${yearEnd}&year_start=${yearStart}`, {
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

    render() {
        const { unemploymentDataPoints, populationDataPoints } = this.state;

        const options1 = {
            title: {
                text: "Unemployment Rate"
            },
            axisX: {
                title: "Year",
                valueFormatString: "YYYY" // Formatowanie wartości osi X jako pełnych lat
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
                valueFormatString: "YYYY" // Formatowanie wartości osi X jako pełnych lat
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
            <div className='container'>
                <CanvasJSChart options={options1} />
                <CanvasJSChart options={options2} />
            </div>
        );
    }
}

export default Graph1;
