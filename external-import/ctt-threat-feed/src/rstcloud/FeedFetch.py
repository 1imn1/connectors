import zlib

import requests


class Downloader:
    def __init__(self, conf):
        # connection
        self.api_url = str(conf.get("baseurl", "https://api.cyberthreattech.ru/v1/")).rstrip(
            "/"
        )
        self.api_key = str(conf.get("apikey", "REPLACEME"))
        self.timeout = (
            int(conf.get("contimeout", 30)),
            int(conf.get("readtimeout", 60)),
        )
        self.retry = int(conf.get("retry", 5))
        self.verify = bool(conf.get("ssl_verify", True))
        self.proxy = str(conf.get("proxy", ""))
        self.time_range = str(conf.get("latest", "latest"))

    def get_feed(self, ioctype: str, path="", filetype="json"):
        fdate = self.time_range
        mapping = {
            "day": "latest",
            "1h": "1h_latest",
            "4h": "4h_latest",
            "12h": "12h_latest",
        }
        date_value = mapping.get(fdate, fdate)
        date_candidates = [date_value]
        if date_value.endswith("_latest"):
            date_candidates.append(date_value.replace("_latest", ""))

        if not path:
            path = f"threatfeed_{ioctype}_{date_value}.{filetype}.gz"

        headers = {
            "User-Agent": "opencti_ctt_threat_feed",
            "Accept": "application/json",
            # Some gateways are case-sensitive on header keys; send both variants.
            "X-Api-Key": self.api_key,
            "x-api-key": self.api_key,
        }
        proxies = {"https": self.proxy} if self.proxy else None

        attempts = []
        for param_name in ("date", "period"):
            for candidate in date_candidates:
                apiurl = f"{self.api_url}/{ioctype}"
                try:
                    r = requests.get(
                        apiurl,
                        headers=headers,
                        proxies=proxies,
                        timeout=self.timeout,
                        params={"type": filetype, param_name: candidate},
                    )
                except Exception as ex:
                    return {
                        "status": "error",
                        "message": str(ex),
                        "url": apiurl,
                        "params": {"type": filetype, param_name: candidate},
                    }

                if r.status_code == 200:
                    try:
                        data = zlib.decompress(r.content, 16 + zlib.MAX_WBITS)
                        with open(path, "wb") as f:
                            f.write(data)
                        return {
                            "status": "ok",
                            "message": path,
                            "url": r.url,
                            "code": r.status_code,
                        }
                    except Exception as ex:
                        return {
                            "status": "error",
                            "message": str(ex),
                            "url": r.url,
                            "code": r.status_code,
                        }

                try:
                    error_body = r.json()
                except ValueError:
                    error_body = r.text
                attempts.append(
                    {
                        "url": r.url,
                        "code": r.status_code,
                        "body": error_body,
                    }
                )

        return {
            "status": "error",
            "message": attempts,
        }
