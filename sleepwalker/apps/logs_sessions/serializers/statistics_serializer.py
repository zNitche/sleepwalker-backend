from rest_framework import serializers


class StatisticsSerializer(serializers.Serializer):
    first_session_start_date = serializers.DateTimeField()
    last_session_start_date = serializers.DateTimeField()
    first_session_end_date = serializers.DateTimeField()
    last_session_end_date = serializers.DateTimeField()
    logs_sessions = serializers.IntegerField()

    sleepwalking_events = serializers.DictField()
    sleepwalking_events_count = serializers.IntegerField()

    class Meta:
        fields = ["logs_sessions",
                  "first_session_start_date",
                  "first_session_end_date",
                  "first_session_end_date",
                  "last_session_end_date",
                  "sleepwalking_events",
                  "sleepwalking_events_count"
                  ]
