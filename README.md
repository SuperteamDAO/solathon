<p align="center">
  <a href="#">
    <img
      alt="Solathon logo"
      src="https://media.discordapp.net/attachments/807140294764003350/929017682836193410/logo.png"
      width="140"
    />
  </a>
</p>


<p align="center">
  <a href="https://pypi.org/project/solathon/" target="_blank"><img src="https://badge.fury.io/py/solathon.svg" alt="PyPI version"></a>
  <a href="https://deepsource.io/gh/GitBolt/solathon/?ref=repository-badge}" target="_blank"><img src="https://deepsource.io/gh/GitBolt/solathon.svg/?label=active+issues&show_trend=true&token=O-2BAnF5y1x-YJyaIe-p4hsK" alt="DeepSource" /></a>
  <a href="https://github.com/GitBolt/solathon/blob/master/LICENSE" target="_blank"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
  <br>
</p>

<h1 align="center">Solathon</h1>

Solathon is an high performance, easy to use and feature-rich Solana SDK for Python. Easy for beginners, powerful for real world applications.

|🧪| The project is in beta phase|
|---|-----------------------------|

# ✨ Getting started
## Installation
```
pip install solathon
```
## Client example
```python
from solathon import Client

client = Client("https://api.devnet.solana.com")
```
## Basic usage example
```python
# Basic example on generating a random public key and fetching it's balance
from solathon import Client, PublicKey

client = Client("https://api.devnet.solana.com")
public_key = PublicKey(1) # Creating a random public key

balance = client.get_balance(public_key)
print(balance)
```

# 🗃️ Contribution
Just drop a pull request lol
