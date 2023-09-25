import asyncio
import logging
import aiohttp

from datetime import datetime, timedelta



logging.basicConfig(level=logging.INFO)


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    r = await response.json()
                    return r
                logging.error(f"Error satatus:{response} for {url}")
                return None
            
        except aiohttp.ClientConnectorError as e:
            logging.error(f"Connection error {url}: {e}")
            
        return None

async def get_exchange(date):
    formatted_date = date.strftime('%d.%m.%Y')
    response_text = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={formatted_date}')
    
    if response_text is not None:
        exchange_rates = {}
        for rate in response_text['exchangeRate']:
            if rate['currency'] in ['EUR', 'USD']:
                exchange_rates[rate['currency']] = {
                    'sale': float(rate['saleRate']),
                    'purchase': float(rate['purchaseRate'])
                }
        return {formatted_date: exchange_rates}
    else:
        return None

async def main():
    number_days= 2
    exchange_rates_list = []
    
    for i  in range(number_days):
        date = datetime.now() - timedelta(days=i)
        exchange_rate = await get_exchange(date)
        exchange_rates_list.append(exchange_rate)
    print(exchange_rates_list)


if __name__ == '__main__':
    asyncio.run(main())