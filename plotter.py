#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np


value_acc_x_signed = []
value_acc_y_signed = []
value_acc_z_signed = []

value_gyr_x_signed = []
value_gyr_y_signed = []
value_gyr_z_signed = []


def init():
    plt.ion()
    plt.figure()
    plt.show()


def convertBytetoDec(bytex1, bytex2, bytey1, bytey2, bytez1, bytez2):

    acc_x_bytes_1 = int(bytex1).to_bytes(1, byteorder='little')
    acc_x_bytes_2 = int(bytex2).to_bytes(1, byteorder='little')
    acc_x_bytes_combined = acc_x_bytes_2 + acc_x_bytes_1
    acc_x_signed_int = int.from_bytes(
        acc_x_bytes_combined, byteorder='little', signed=True)
    value_acc_x_signed.append(acc_x_signed_int)

    acc_y_bytes_1 = int(bytey1).to_bytes(1, byteorder='little')
    acc_y_bytes_2 = int(bytey2).to_bytes(1, byteorder='little')
    acc_y_bytes_combined = acc_y_bytes_2 + acc_y_bytes_1
    acc_y_signed_int = int.from_bytes(
        acc_y_bytes_combined, byteorder='little', signed=True)
    value_acc_y_signed.append(acc_y_signed_int)

    acc_z_bytes_1 = int(bytez1).to_bytes(1, byteorder='little')
    acc_z_bytes_2 = int(bytez2).to_bytes(1, byteorder='little')
    acc_z_bytes_combined = acc_z_bytes_2 + acc_z_bytes_1
    acc_z_signed_int = int.from_bytes(
        acc_z_bytes_combined, byteorder='little', signed=True)
    value_acc_z_signed.append(acc_z_signed_int)


def plot():
    # Plot accelerometer and gyroscope values
    plt.clf()
    plt.plot(value_acc_x_signed, 'r', label='x-Achse')
    plt.plot(value_acc_y_signed, 'g', label='y-Achse')
    plt.plot(value_acc_z_signed, 'b', label='z-Achse')
    plt.title('Accelerometer: Bewegungsart, Sensorposition: Handgelenk / Gürtel')
    plt.xlabel('Messwert-Nummer')
    plt.ylabel('Beschleunigung in mg')
    plt.legend(loc='best')
    plt.draw()
    plt.pause(0.1)
