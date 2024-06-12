import React, { Component } from 'react';
import CanvasJSReact from '@canvasjs/react-charts';
import axios from 'axios';

const CanvasJSChart = CanvasJSReact.CanvasJSChart;

class Graph4 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            internetUsersDataPoints: [],
            internetUsersPercentDataPoints: [],
            userRole: null
        };
    }

    componentDidMount() {
        this.fetchInternetUsersData();
        this.fetchUserRole();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.selectedCountry !== this.props.selectedCountry || prevProps.yearRange !== this.props.yearRange) {
            this.fetchInternetUsersData();
        }
    }

    fetchInternetUsersData = async () => {
        const { selectedCountry, yearRange } = this.props;
        if (!selectedCountry) return;

        const currentYear = 2020;
        const yearStart = currentYear - yearRange + 1;
        const yearEnd = currentYear;

        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`http://127.0.0.1:8001/api/internet`, {
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

            const data = response.data;
            const internetUsersDataPoints = data.values.map(item => ({
                x: new Date(item.year, 0, 1),
                y: item.internetusersnumber
            }));
            const internetUsersPercentDataPoints = data.values.map(item => ({
                x: new Date(item.year, 0, 1),
                y: item.internetuserspercent
            }));
            this.setState({ internetUsersDataPoints, internetUsersPercentDataPoints });
        } catch (error) {
            console.error('Error fetching internet users data', error);
        }
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
            console.error('Error fetching user groups', error);
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
        const { internetUsersDataPoints, internetUsersPercentDataPoints, userRole } = this.state;

        const options1 = {
            title: {
                text: "Internet Users"
            },
            axisX: {
                title: "Year",
                valueFormatString: "YYYY"
            },
            axisY: {
                title: "Number of Internet Users"
            },
            data: [{
                type: "column",
                dataPoints: internetUsersDataPoints
            }]
        };

        const options2 = {
            title: {
                text: "Percentage of Internet Users"
            },
            axisX: {
                title: "Year",
                valueFormatString: "YYYY"
            },
            axisY: {
                title: "Percentage (%)"
            },
            data: [{
                type: "column",
                dataPoints: internetUsersPercentDataPoints
            }]
        };

        return (
            <div>
                <div className='container'>
                    {userRole === 'export' && (
                        <button 
                        onClick={() => this.downloadDataAsJson(internetUsersDataPoints, 'internet_users_data.json')}
                        style={{ marginBottom: '20px' }}
                    >
                        Download Internet Users Data as JSON
                    </button>
                    )}
                    <CanvasJSChart options={options1} />
                </div>
                <div className='container'>
                    {userRole === 'export' && (
                        <button 
                        onClick={() => this.downloadDataAsJson(internetUsersPercentDataPoints, 'internet_users_percent_data.json')}
                        style={{ marginBottom: '20px' }}
                    >
                        Download Internet Users Percent Data as JSON
                    </button>
                    )}
                    <CanvasJSChart options={options2} />
                </div>
            </div>
        );
    }
}

export default Graph4;
