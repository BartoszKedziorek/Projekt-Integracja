import React, { Component } from 'react';
import axios from 'axios';

class Graph3 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            populationData: [],
            unemployedData: [],
            internetData: [],
            isLoading: true,
            userRole: '',
        };
    }

    componentDidMount() {
        this.fetchData('populationData', 'population/extreme');
        this.fetchData('unemployedData', 'unemployment/extreme');
        this.fetchData('internetData', 'internet/extreme');
        this.fetchUserRole();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.extreme_type !== this.props.extreme_type || prevProps.years !== this.props.years) {
            this.fetchData('populationData', 'population/extreme');
            this.fetchData('unemployedData', 'unemployment/extreme');
            this.fetchData('internetData', 'internet/extreme');
        }
    }

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

    fetchData = async (dataKey, endpoint) => {
        try {
            this.setState({ isLoading: true });
            const token = localStorage.getItem('token');
            const response = await axios.get(`http://127.0.0.1:8001/api/${endpoint}`, {
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                },
                params: {
                    amount: 10,
                    extreme_type: this.props.extreme_type,
                    years: this.props.years,
                },
            });

            if (response.data && response.data.length > 0) {
                const dataPoints = response.data.map(item => ({
                    name: item.name,
                    value: parseFloat(item.value),
                }));

                this.setState({ [dataKey]: dataPoints, isLoading: false });
            } else {
                this.setState({ [dataKey]: [], isLoading: false });
            }
        } catch (error) {
            console.error(`Error fetching ${dataKey} data`, error);
            this.setState({ isLoading: false });
        }
    };

    downloadDataAsJson = (data, filename) => {
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        URL.revokeObjectURL(url);
    };

    render() {
        const { populationData, unemployedData, internetData, userRole } = this.state;

        return (
            <div style={styles.dataContainer}>
                <div>
                    {userRole === 'export' && (
                        <button
                            onClick={() => this.downloadDataAsJson(populationData, 'population_data_top10.json')}
                            style={styles.downloadButton}
                        >
                            Download Population Data as JSON
                        </button>
                    )}
                    <table style={styles.styledTable}>
                        <thead style={styles.tableHeader}>
                            <tr>
                                <th style={styles.tableCell}>Country</th>
                                <th style={styles.tableCell}>Population Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {populationData.map((item, index) => (
                                <tr
                                    key={index}
                                    style={{
                                        ...styles.tableRow,
                                        ...(index % 2 === 0 ? styles.tableRowEven : {}),
                                    }}
                                >
                                    <td style={styles.tableCell}>{item.name}</td>
                                    <td style={styles.tableCell}>{item.value}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div>
                    {userRole === 'export' && (
                        <button
                            onClick={() => this.downloadDataAsJson(unemployedData, 'unemployed_data_top10.json')}
                            style={styles.downloadButton}
                        >
                            Download Unemployed Data as JSON
                        </button>
                    )}
                    <table style={styles.styledTable}>
                        <thead style={styles.tableHeader}>
                            <tr>
                                <th style={styles.tableCell}>Country</th>
                                <th style={styles.tableCell}>Unemployed Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {unemployedData.map((item, index) => (
                                <tr
                                    key={index}
                                    style={{
                                        ...styles.tableRow,
                                        ...(index % 2 === 0 ? styles.tableRowEven : {}),
                                    }}
                                >
                                    <td style={styles.tableCell}>{item.name}</td>
                                    <td style={styles.tableCell}>{item.value != null ? `${item.value.toFixed(2)}%` : ''}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div>
                    {userRole === 'export' && (
                        <button
                            onClick={() => this.downloadDataAsJson(internetData, 'internet_data_top10.json')}
                            style={styles.downloadButton}
                        >
                            Download Internet Data as JSON
                        </button>
                    )}
                    <table style={styles.styledTable}>
                        <thead style={styles.tableHeader}>
                            <tr>
                                <th style={styles.tableCell}>Country</th>
                                <th style={styles.tableCell}>Internet Users</th>
                            </tr>
                        </thead>
                        <tbody>
                            {internetData.map((item, index) => (
                                <tr
                                    key={index}
                                    style={{
                                        ...styles.tableRow,
                                        ...(index % 2 === 0 ? styles.tableRowEven : {}),
                                    }}
                                >
                                    <td style={styles.tableCell}>{item.name}</td>
                                    <td style={styles.tableCell}>{item.value != null ? `${item.value.toFixed(2)}%` : ''}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}

const styles = {
    dataContainer: {
        padding: '20px',
        display: 'flex',
        justifyContent: 'space-around', // Adjust as needed
        alignItems: 'center',
        flexDirection: 'row', // Align tables horizontally
        flexWrap: 'wrap', // Allow wrapping for smaller screens
    },
    downloadButton: {
        padding: '10px 20px',
        marginBottom: '20px',
        backgroundColor: '#28a745',
        color: '#ffffff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
    },
    styledTable: {
        borderCollapse: 'collapse',
        margin: '0 10px', // Adjust spacing between tables
        fontSize: '18px',
        minWidth: '400px',
        boxShadow: '0 0 20px rgba(0, 0, 0, 0.15)',
        backgroundColor: '#f8f9fa',
    },
    tableHeader: {
        backgroundColor: '#007bff',
        color: '#ffffff',
    },
    tableCell: {
        padding: '12px 15px',
        border: '1px solid #dddddd',
    },
    tableRow: {
        borderBottom: '1px solid #dddddd',
    },
    tableRowEven: {
        backgroundColor: '#e9ecef',
    },
    tableRowLast: {
        borderBottom: '2px solid #007bff',
    },
    activeRow: {
        fontWeight: 'bold',
        color: '#007bff',
    },
};

export default Graph3;
