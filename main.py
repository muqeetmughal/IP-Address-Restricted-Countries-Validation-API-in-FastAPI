from fastapi import FastAPI, HTTPException, Request
import httpx
from pydantic import BaseModel, ValidationError, validator
from typing import Union


app = FastAPI()


class InfoDetails(BaseModel):
    ip: str
    city: str
    region: str
    country: str
    loc: str
    org: str
    postal: str
    timezone: str


class ResponseModel(BaseModel):
    allowed: bool
    message: str
    info: InfoDetails


class IPAddressValidator(BaseModel):
    ip_address: str

    @validator("ip_address")
    def validate_ip_address(cls, value):
        try:
            ip_parts = value.split(".")
            if len(ip_parts) != 4:
                raise ValueError("Invalid IP address format")

            for part in ip_parts:
                if not 0 <= int(part) <= 255:
                    raise ValueError("Invalid IP address format")

            return value

        except ValueError as e:
            raise ValueError(f"Invalid IP address format: {e}")


RESTRICTED_COUNTRIES = [
    "CA",  # Ontario, Canada
    "US",  # United States
    "AS",  # American Samoa
    "GU",  # Guam
    "MP",  # Northern Mariana Islands
    "PR",  # Puerto Rico
    "VI",  # U.S. Virgin Islands
    "FR",  # France
    "GF",  # French Guiana
    "PF",  # French Polynesia
    "GP",  # Guadeloupe
    "MQ",  # Martinique
    "YT",  # Mayotte
    "RE",  # Reunion
    "BL",  # Saint Barthelemy
    "MF",  # Saint Martin
    "PM",  # Saint Pierre and Miquelon
    "WF",  # Wallis and Futuna
    "NL",  # Netherlands
    "AW",  # Aruba
    "CW",  # Curacao
    "SX",  # St. Maarten
    "BQ",  # Bonaire
    "SS",  # St. Eustatius
    "SB",  # Saba
    "TR",  # Turkey
    "CU",  # Cuba
    "IR",  # Iran
    "KP",  # North Korea
    "KR",  # South Korea
    "SD",  # Sudan
    "SY",  # Syria
    "UA",  # Ukraine
    "RU",  # Russia
]


@app.get("/")
async def validate_ip(request: Request):
    client_host = request.client.host
    print(client_host)
    return client_host


async def get_country_by_ip(ip: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data
    except Exception as e:
        print(f"Error getting country for IP {ip}: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"Error getting country for IP {ip}",
            },
        )


@app.get("/check_country", response_model=ResponseModel)
async def check_country(ip: str):
    try:
        ip_parts = ip.split(".")
        if len(ip_parts) != 4:
            raise HTTPException(
                status_code=400, detail=str("Invalid IP address format")
            )

        for part in ip_parts:
            if not 0 <= int(part) <= 255:
                raise HTTPException(
                    status_code=400, detail=str("Invalid IP address format")
                )
        try:
            data = await get_country_by_ip(ip)
            del data["readme"]

            country = data.get("country", "")
            if country in RESTRICTED_COUNTRIES:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "message": f"Access restricted for your country {country}.",
                        "info": data,
                        "allowed": False,
                    },
                )

            return {
                "message": "Access allowed.",
                "info": data,
                "allowed": True,
            }

        except HTTPException as e:
            raise e  # Re-raise HTTPException to let FastAPI handle it
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    except ValueError as e:
        raise ValueError(f"Invalid IP address format: {e}")
