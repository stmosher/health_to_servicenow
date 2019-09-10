import pytest
from h_s_classes.health_insights import HealthInsights


data = [{
    "series": [{
        "columns": [
            "time",
            "activation_threshold",
            "alert_src",
            "clear_threshold",
            "crit_threshold",
            "id",
            "kpi_stream",
            "msg",
            "sigma",
            "warn_threshold"
        ],
        "name": "alerts",
        "tags": {
            "CollectorId": "mdt-robot-collector-13a3958e-63d5-47e5-9e0f-31e846b89f2e",
            "EncodingPath": "Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization",
            "Producer": "spnac-a9k-s079",
            "UUID": "5108e98e-aea0-49a5-ba32-88db39b777c3",
            "kpi_id": "pulse_cpu_utilization",
            "level": "INFO",
            "node-name": "0/RP0/CPU0",
            "state": "clear"
        },
        "values": [
            [
                "2019-09-05T22:02:57.412Z",
                -1,
                "TICK",
                2,
                2,
                "pulse_cpu_utilization",
                2,
                "INFO : 0/RP0/CPU0  5min CPU Utilization: 2.00 % has returned to Usual range, Threshold: 2.00 SD. It is 0.45 std. dev away from Average.",
                0.45390323755854023,
                2
            ]
        ]
    }]
}]


@pytest.fixture()
def health_insights_obj():
    return HealthInsights()


def test_parse_alert_body(health_insights_obj):
    assert health_insights_obj.parse_alert_body(data) == [
        {'id': 'pulse_cpu_utilization', 'kpi_id': 'pulse_cpu_utilization', 'level': 'INFO',
         'msg': 'INFO : 0/RP0/CPU0  5min CPU Utilization: 2.00 % has returned to Usual range, Threshold: 2.00 SD. It is 0.45 std. dev away from Average.',
         'producer': 'spnac-a9k-s079', 'state': 'clear', 'time': '2019-09-05T22:02:57.412Z',
         'uuid': '5108e98e-aea0-49a5-ba32-88db39b777c3'}]


def test_parse_alert_body_value_error(health_insights_obj):
    assert health_insights_obj.parse_alert_body([{"series": [{"missing_columns": ''}]}]) is False


if __name__ == '__main__':
    import pytest
    pytest.main(['-s', '--color=yes', 'test_health_insights.py'])
