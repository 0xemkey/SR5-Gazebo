# Logitech F710 Mapping

The Windows publisher is `tools/windows/gamepad_sender_50hz.py`. It uses Python package `inputs` and sends JSON state over UDP.

## Transport
| Parameter | Value |
|---|---|
| Protocol | UDP |
| Destination port | 9090 |
| Send frequency | 50 Hz |
| Axes array | 8 values |
| Buttons array | 15 values |

## Axes
| Input | Index |
|---|---|
| Left stick X | `axes[0]` |
| Left stick Y | `axes[1]` |
| Right stick X | `axes[2]` |
| Right stick Y | `axes[3]` |
| Left trigger | `axes[4]` |
| Right trigger | `axes[5]` |
| D-pad X | `axes[6]` |
| D-pad Y | `axes[7]` |

The publisher inverts both stick Y axes and D-pad Y.

## Buttons
| Input | Index |
|---|---|
| A | `buttons[0]` |
| B | `buttons[1]` |
| X | `buttons[2]` |
| Y | `buttons[3]` |
| LB | `buttons[4]` |
| RB | `buttons[5]` |
| Select | `buttons[6]` |
| Start | `buttons[7]` |
| Left stick click | `buttons[9]` |
| Right stick click | `buttons[10]` |

LB is assigned as the left-arm deadman control; RB is assigned as the right-arm deadman control. Actual Cartesian directions and motion limits are defined by the IK implementation.
