import React, { Component } from 'react';
import CanvasJSReact from '@canvasjs/react-charts';

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

class Graph4 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            internetUsersDataPoints: [],
            percentDataPoints: []
        };
    }

    componentDidMount() {
        this.generateExampleData();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.selectedCountry !== this.props.selectedCountry || prevProps.yearRange !== this.props.yearRange) {
            this.generateExampleData();
        }
    }

    generateExampleData = () => {
        // Generate example data for internet users and percentage
        const { yearRange } = this.props;
        const internetUsersDataPoints = [];
        const percentDataPoints = [];
        const currentYear = new Date().getFullYear();
        const startYear = currentYear - yearRange + 1; // Początkowy rok na osi X
        const endYear = currentYear; // Końcowy rok na osi X
        for (let year = startYear; year <= endYear; year++) {
            internetUsersDataPoints.push({ x: new Date(year, 0, 1), y: Math.floor(Math.random() * 1000) }); // Random number of internet users
            percentDataPoints.push({ x: new Date(year, 0, 1), y: Math.random() * 100 }); // Random percentage
        }
        this.setState({ internetUsersDataPoints, percentDataPoints });
    };

    render() {
        const { internetUsersDataPoints, percentDataPoints } = this.state;

        const options1 = {
            title: {
                text: "Internet Users"
            },
            axisX: {
                title: "Date Range",
                valueFormatString: "YYYY" // Formatowanie wartości osi X jako pełnych lat
            },
            axisY: {
                title: "Number of Internet Users"
            },
            data: [{
                type: "column", // zmieniony typ wykresu na słupkowy
                dataPoints: internetUsersDataPoints
            }]
        };

        const options2 = {
            title: {
                text: "Percentage"
            },
            axisX: {
                title: "Date Range",
                valueFormatString: "YYYY" // Formatowanie wartości osi X jako pełnych lat
            },
            axisY: {
                title: "Percent (%)"
            },
            data: [{
                type: "column", // zmieniony typ wykresu na słupkowy
                dataPoints: percentDataPoints
            }]
        };

        return (
            <div>
                <div className='container'>
                    <CanvasJSChart options={options1} />
                </div>
                <div className='container'>
                    <CanvasJSChart options={options2} />
                </div>
            </div>
        );
    }
}

export default Graph4;
