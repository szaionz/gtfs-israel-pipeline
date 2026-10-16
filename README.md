# Pipeline for public transportation data in Israel
Process [publicly available GTFS data](https://a.com) for public transit navigation, for ingestion by [OpenTripPlanner](https://github.com/opentripplanner/OpenTripPlanner)

## Quickstart
Run the backend:
```bash
docker build -t otp-israel --file Dockerfile.otp .
docker run --rm -d -p 8080:8080 otp-israel
```