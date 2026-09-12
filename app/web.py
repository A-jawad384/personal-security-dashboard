from flask import Flask, request, redirect
from database import (
    initialize_database,
    get_event_count,
    get_all_events,
    get_all_alerts,
    get_events_by_severity,
    get_severity_count,
    resolve_alert
)

app = Flask(__name__)

initialize_database()


def severity_class(severity):
    return severity.lower()


@app.route("/resolve-alert/<int:alert_id>", methods=["POST"])
def resolve_alert_route(alert_id):
    from database import resolve_alert

    resolve_alert(alert_id)

    return redirect(request.referrer or "/")

@app.route("/")
def dashboard():
    event_count = get_event_count()
    severity = request.args.get("severity")

    low_count = get_severity_count("LOW")
    medium_count = get_severity_count("MEDIUM")
    high_count = get_severity_count("HIGH")
    critical_count = get_severity_count("CRITICAL")

    if severity:
        events = get_events_by_severity(severity)
    else:
        events = get_all_events()

    displayed_event_count = len(events)

    alerts = get_all_alerts()

    new_alerts = sum(1 for alert in alerts if alert[5] == "NEW")
    critical_events = sum(1 for event in events if event[3] == "CRITICAL")
    high_events = sum(1 for event in events if event[3] == "HIGH")

    html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>PSMD | Security Monitoring Dashboard</title>

        <style>

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, Helvetica, sans-serif;
                background: #0f172a;
                color: #e2e8f0;
            }

            .container {
                width: 95%;
                max-width: 1500px;
                margin: 0 auto;
            }

            header {
                padding: 30px 0;
                border-bottom: 1px solid #334155;
            }

            .header-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 20px;
            }

            .brand h1 {
                margin: 0;
                font-size: 28px;
            }

            .brand p {
                margin: 8px 0 0;
                color: #94a3b8;
            }

            .status {
                display: flex;
                align-items: center;
                gap: 8px;
                background: #172554;
                padding: 10px 15px;
                border-radius: 20px;
                font-size: 14px;
            }

            .status-dot {
                width: 9px;
                height: 9px;
                background: #22c55e;
                border-radius: 50%;
            }

            .dashboard {
                padding: 30px 0;
            }

            .cards {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }

            .card {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 22px;
            }

            .card-title {
                color: #94a3b8;
                font-size: 14px;
                margin-bottom: 12px;
            }

            .card-value {
                font-size: 32px;
                font-weight: bold;
            }

            .card-description {
                margin-top: 8px;
                color: #64748b;
                font-size: 13px;
            }

            .critical {
                color: #ef4444;
            }

            .high {
                color: #f97316;
            }

            .medium {
                color: #eab308;
            }

            .low {
                color: #22c55e;
            }

            .section {
                margin-bottom: 30px;
            }

            .section-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }

            .section-header h2 {
                margin: 0;
                font-size: 20px;
            }

            .badge {
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                font-weight: bold;
            }

            .badge-new {
                background: #450a0a;
                color: #fca5a5;
            }

            .badge-resolved {
                background: #052e16;
                color: #86efac;
            }

            .table-container {
                overflow-x: auto;
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                min-width: 900px;
            }

            th {
                background: #172033;
                color: #94a3b8;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            th, td {
                padding: 14px 16px;
                border-bottom: 1px solid #334155;
                text-align: left;
            }

            td {
                font-size: 14px;
            }

            tr:last-child td {
                border-bottom: none;
            }

            .severity-badge {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
            }

            .severity-critical {
                background: #450a0a;
                color: #fca5a5;
            }

            .severity-high {
                background: #431407;
                color: #fdba74;
            }

            .severity-medium {
                background: #422006;
                color: #fde68a;
            }

            .severity-low {
                background: #052e16;
                color: #86efac;
            }

            footer {
                padding: 25px 0;
                border-top: 1px solid #334155;
                color: #64748b;
                font-size: 13px;
                text-align: center;
            }

            @media (max-width: 900px) {

                .cards {
                    grid-template-columns: repeat(2, 1fr);
                }

                .header-content {
                    flex-direction: column;
                    align-items: flex-start;
                }
            }

            @media (max-width: 600px) {

                .cards {
                    grid-template-columns: 1fr;
                }

                .container {
                    width: 92%;
                }
            }

        </style>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>

    <body>

        <header>
            <div class="container header-content">

                <div class="brand">
                    <h1>🛡️ Personal Security Monitoring Dashboard</h1>
                    <p>Security event monitoring and alert management</p>
                </div>

                <div class="status">
                    <span class="status-dot"></span>
                    Monitoring Active
                </div>

            </div>
        </header>


        <main class="container dashboard">

            <div class="cards">

                <div class="card">
                    <div class="card-title">TOTAL SECURITY EVENTS</div>
                    <div class="card-value">""" + str(event_count) + """</div>
                    <div class="card-description">Recorded events</div>
                </div>

                <div class="card">
                    <div class="card-title">TOTAL ALERTS</div>
                    <div class="card-value">""" + str(len(alerts)) + """</div>
                    <div class="card-description">Generated alerts</div>
                </div>

                <div class="card">
                    <div class="card-title">ACTIVE ALERTS</div>
                    <div class="card-value critical">""" + str(new_alerts) + """</div>
                    <div class="card-description">Requires attention</div>
                </div>

                <div class="card">
                    <div class="card-title">HIGH / CRITICAL EVENTS</div>
                    <div class="card-value high">""" + str(high_events + critical_events) + """</div>
                    <div class="card-description">Higher-risk events</div>
                     </div>

                <div style="margin-top: 25px;">
                    <canvas id="severityChart"></canvas>
                </div>

            </div>


            <div class="section">

                <div class="section-header">
                    <h2>🚨 Security Alerts</h2>
                    <span class="badge badge-resolved">
                        Events by Severity
                    </span>
                </div>

                <div class="cards">

                    <div class="card">
                        <div class="card-title">LOW</div>
                        <div class="card-value">
                            """ + str(low_count) + """
                        </div>
                        <div class="card-description">
                            Low-risk events
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-title">MEDIUM</div>
                        <div class="card-value">
                            """ + str(medium_count) + """
                        </div>
                        <div class="card-description">
                            Moderate-risk events
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-title">HIGH</div>
                        <div class="card-value high">
                            """ + str(high_count) + """
                        </div>
                        <div class="card-description">
                            High-risk events
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-title">CRITICAL</div>
                        <div class="card-value critical">
                            """ + str(critical_count) + """
                        </div>
                        <div class="card-description">
                            Critical events
                        </div>
                    </div>

                </div>

            </div>



                <div style="margin: 15px 0;">
    <form method="get">
        <label for="severity"><strong>Filter by Severity:</strong></label>

        <select name="severity" id="severity" onchange="this.form.submit()">
            <option value="">All Severities</option>
            <option value="LOW">LOW</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="HIGH">HIGH</option>
            <option value="CRITICAL">CRITICAL</option>
        </select>
    </form>
</div>

                    <table>

                        <tr>
                            <th>ID</th>
                            <th>Timestamp</th>
                            <th>Alert Type</th>
                            <th>Severity</th>
                            <th>Message</th>
                            <th>Status</th>
                        </tr>
        """

    for alert in alerts:

        status_class = "badge-new" if alert[5] == "NEW" else "badge-resolved"

        html += f"""
                        <tr>
                            <td>{alert[0]}</td>
                            <td>{alert[1]}</td>
                            <td>{alert[2]}</td>

                            <td>
                                <span class="severity-badge severity-{severity_class(alert[3])}">
                                    {alert[3]}
                                </span>
                            </td>

                            <td>{alert[4]}</td>

                     <td>
    <span class="badge {status_class}">
        {alert[5]}
    </span>

  {"<form method='POST' action='/resolve-alert/" + str(alert[0]) + "' style='display:inline;'><button type='submit' class='resolve-button'>Resolve</button></form>" if alert[5] == "NEW" else ""}
</td>   
                            
                                    
                                
                        
                        </tr>
        """

    html += """

                    </table>

                </div>

            </div>


            <div class="section">

             <div class="section-header">

    <div>
        <h2>🔐 Security Events</h2>

        <form method="GET" style="margin-top: 10px;">

            <label for="severity">
                <strong>Filter by Severity:</strong>
            </label>

            <select name="severity" id="severity" onchange="this.form.submit()">

                <option value="">All Severities</option>

                <option value="LOW" """ + ("selected" if severity == "LOW" else "") + """>
                    LOW
                </option>

                <option value="MEDIUM" """ + ("selected" if severity == "MEDIUM" else "") + """>
                    MEDIUM
                </option>

                <option value="HIGH" """ + ("selected" if severity == "HIGH" else "") + """>
                    HIGH
                </option>

                <option value="CRITICAL" """ + ("selected" if severity == "CRITICAL" else "") + """>
                    CRITICAL
                </option>

            </select>

        </form>
    </div>

    <span class="badge badge-resolved">
        """ + str(displayed_event_count) + (" Event" if displayed_event_count == 1 else " Events") + """
    </span>

</div>

                <div class="table-container">

                    <table>

                        <tr>
                            <th>ID</th>
                            <th>Timestamp</th>
                            <th>Event Type</th>
                            <th>Severity</th>
                            <th>Source</th>
                            <th>Message</th>
                        </tr>
        """

    for event in events:

        html += f"""
                        <tr>

                            <td>{event[0]}</td>

                            <td>{event[1]}</td>

                            <td>{event[2]}</td>

                            <td>
                                <span class="severity-badge severity-{severity_class(event[3])}">
                                    {event[3]}
                                </span>
                            </td>

                            <td>{event[4]}</td>

                            <td>{event[5]}</td>

                        </tr>
        """

    html += """

                    </table>

                </div>

            </div>

        </main>


        <footer>

            Personal Security Monitoring Dashboard
            | Defensive Security Project
            | Flask + SQLite + Python

        </footer>
                <script>
            const ctx = document.getElementById("severityChart");

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                    datasets: [{
                        label: "Security Events",
                        data: [
                            """ + str(low_count) + """,
                            """ + str(medium_count) + """,
                            """ + str(high_count) + """,
                            """ + str(critical_count) + """
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            });
        </script>

    </body>

    </html>
    """

    return html


if __name__ == "__main__":
    app.run(debug=True)
