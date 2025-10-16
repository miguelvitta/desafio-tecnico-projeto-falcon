import qrcode

def generate_qr_codes():
    qr_stop = qrcode.make("STOP_FALCON")
    qr_stop.save("stop_falcon.png")
    print("QRCode 'STOP_FALCON' generated as stop_falcon.png")

    qr_start = qrcode.make("START_FALCON")
    qr_start.save("start_falcon.png")
    print("QRCode 'START_FALCON' generated as start_falcon.png")


if __name__ == "__main__":
    print("Starting generation of QRCodes for Falcon Vision AI...")
    generate_qr_codes()
    print("Generation finished.")