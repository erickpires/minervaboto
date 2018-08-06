#!/usr/bin/env python3

from minervaboto import renew_books, renewed_to_string, utils
from multiprocessing import Process, Queue

import os
import wx
import wx.lib.dialogs
import wx.lib.embeddedimage

__LOGO__ = wx.lib.embeddedimage.PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAFYAAABVCAYAAADTwhNZAAAABGdBTUEAALGPC/xhBQAAACBj'
    b'SFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+g'
    b'vaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4gceExwypX79YQAAGrNJREFUeNrV'
    b'nUuMJMl5mL8/IjPr2dXv6Zmd3dlZ7nK0u6QoL3fX5lsQZMLiQRYEHyXYsAFffZFh+2To5IMv'
    b'Psi6GIYvBgwYNm0IhkUZOpgwIdJDalfLFcnVkpzlkj2vnn5Vd3U9MzN+HzKzKqsq69XTS8o5'
    b'KHR3VmZE5Bd//PE/InLECypEg64A8ju///WN7dtvftFJ8IVY5RVFGiiiLD50iYt0wd9owbk5'
    b'N1ymXSvXObsMFfTcir5ntP+Nk5/e/cZ//1e/fgao9csqgADmH//BT+549Wf/SS+2vx3Gshe5'
    b'pMAiYLMaJ/N4TFyjM65ZxFV1vIx59S5zT1HbisAWtV0ErAHf6uOKjb8at376B//pn730Y8AJ'
    b'4P39f/29j/lbL/+bTmS/Ekbj5S/scZaU1isoZ5kyVr3nqtruW7TmR/8jPHrn9/7b77/5of38'
    b'3/uXjWuf+K3f60T+70YxZtVKr+q4TF2y+i3TZVxBIaoQOyRW81K5ttXz3fld+4V/+B++EAfb'
    b'/zR0srXoQa9KWq/quIpir7JtTjGK2d3Ye/HPPedvvqHO3FpU2c9ReK/s+HmOuOyInLxggp3X'
    b'vEjNc6J4l2nMZaX1Ms97Gf16FceqnROrBM7Z541z6mcFzCrksirgoy7raeu+TL3L3BIrVaOq'
    b'cyt4GhC/iKH48667cESqilHVmfPiz0O6fl6T31WonxXuFK/w9BVU9FFOgL+ogbBKvWbZmz8K'
    b'qL9QU+0qRsGcMsYkVueUsKwdXeQaFp7TxQb+1DWqy0lNepEAiEzVv8gNLqo7u2dZEl7mO8+r'
    b'wKhDNF4a7DLBkmWDNpmfDopRMDgsjkAdJRweDlFQgQhDD0MfS4whFpO0f4R5tfoLnkPF4MQu'
    b'BrtcwQouQnGzSRVClLFyZgVgJitMgCbSWdGYhg7Yos+NuM1u1GEr7lCNB5TdABs7RB2KEImh'
    b'ZwNaXpkjr8YDb437psaxlOmIhyCIwOz5WiabUnCJASMUaNHFYGcW6hyqbiaZsdMiUyE5Hf6c'
    b'GIwZUAVB8TRmV/vcdi1eDM+43Ttlt3NGvX1B0Ovj9QeYMEbiGOJcewTUWpzvEZYDOrUah2sb'
    b'/LB+jXdK1/ihWactPoogIsxTCJPwh20XRTHJrTIb7riOXRhd0hHcmVALel0y/VTUgYqmOnxN'
    b'Q57XNp8Kj7nTOeLm2TH15hleu4d0QxjGMnOFTxQqqhgRPIGKOWYreMCL6x/y5rUd/mLrFl8v'
    b'3+SeWSPCDuHKMBIjaXuKoWa/q8agKdcZcL1lgE4jdAnkwg6R6ectCiaroiTOSZ2QO3rBG4ND'
    b'Xm0dcO3oiNJpC+kMUpgFzUjGdMEMI6PfY0W6IX63yY3TCzb3mjx3s8kf11/gO3abgXiImCFI'
    b'SSVgWrfmKxHUuaReNxuut7QXNc4EdBzuTKgFhWgKtUTMx7TN58NDPnX2iGuHh/gnF0h3cOmw'
    b'/syT/Yjyg2Ne6Q2o3B7gNV7km3aXUDwEk1oPMqnPpspRZDTXMBvu3Mlr0XPNVwnFX7jUyrjG'
    b'gM+4Yz538ZBbB48pHZ0nQN1HaP5HinfY4rbs85UXDKc1y3fNFhiDqAExBe2X9Fwesss9khTC'
    b'XRnslB2XVwnj7RmdVMUpWBy7GvKqtvhc74CXjx5SPzjBXPQToFfpWczqYpfAfcm7z288H9As'
    b'W36ma8TGIqqokFoPmUUzsmARGY62THaH0jsBd0WwBUNdsvkklxjKGKkiqgQ4nqHPL2mL13rH'
    b'fLz5hMaTE+xZJ9GhK/XsJX3l/DWxIzho8ivBPlwXvlve5TFVzqREE582llANDsElmDGplZMY'
    b'zVmBOckVEmM6PbEc2FFacgZsN5RMTeOPZWJ2CHlBu7wcnfFi95SbpydUT84wrd400KsAtsqN'
    b'g5j6/iGfaXX4G419Lqo1zkoVzkoVjr0qj7wa+6bKQyqcSkBHLSomGbGSNw9HEpulZtW5xWBH'
    b'Gcq83Zn/Xof6VtTRIOJjdPlEdMYrvVOunzdZOzvHP+8kJlORDr1SFbA8ZxnEeE/OqR+1qHuG'
    b'69aggUdcCehXK1zUahzWGvy4ssX3vU3eNw2OqCQUM1s2IZmokFR0VeeAXRT01uFHEXVsa59X'
    b'9YJPhyd8/PyQ7ZNTgrP2yP5ctaJLQ70EfKfQj0FjpB3iNbt4ckbdGq5VfO40qrx5bZdvbd3i'
    b'q/5tTsSSRSBUXaKPnaKioA4mwS5s+9AwT5S2qlLTiF/Wcz43eMLLpwdsHJ7gnXVgEK1uMq3K'
    b'5rKqYla9eVXnFHUxEsYE512e6fT4eLlMo77HsZTTEZxNaCApVJVk9HrzUjJTjUl1qKIYdTyn'
    b'HX4tPOCN5gN2Hx7gNdsQLjkZPW0e6LK69TK3BR7dRpWfSMCRAzRGxUC2TGjMqSiQ2HkVjwIj'
    b'iq8Rr7lT/s7Fz7jz6D6Vgyb0whUe5KOQ1CvS0/nwnG9xjTLN3XW+tb7DH5ttLvASsGpG8YbU'
    b'A0x+JGLvLa5Dh3pUUda1zxfDR3z56B7XHzzEnnZWM+pXhfpRJ6+yyUIAK+BZ4rJPuFai2ahx'
    b'r1rjrlnjrtmiadeHwaXhCBZFkHF7V5WlUjOZtO64Hl/p/ZRfffQjGvcPkPZgxYe4AqiXkdac'
    b'FA7VqBHUGtS3uJJHWAnoVko0KyUOgoB7JuA9LfOB1Dgya2hQxRovdZBykopL1UKiGhLeKdh5'
    b'8dFMWvdch9/s3uML9/+K6v4h9KLV1vj8IqAaST7WoJ4h9i1R4DEIfPpln5bvc+z7HFifA/F4'
    b'rB738TmkRJsSAxsgXgljfYzxwNgkaGNsLtiTMkonsuzwFg40VdbcgF8N7/NG5wHlQR9XDZCy'
    b'h8QKYZx85qmDj2r4p7pNBNQI6tnEDg08wpJPWPLoBT4d36PreXStoW8tZ1jeCS37zqclPk18'
    b'euLjjAfGB2MwYrDGIsZDjIX0pxpL6vSmjZAUrkuDOSnYue1OY6W1uEOne8ZbJqC0dw1zzVF2'
    b'MfU4Zj0MWWv3qZx3sOe9JPD8UUDNnxYBz+BKlqgS0KsE9ColOiWftufRtpaOETqi9I3SxzEQ'
    b'Ryx9YnF04irvxDs8sWWMsZhUEm0a5UIMIiYBKjb529j07+S7YTuGbcskN9Gz8zMIabjzkVT4'
    b'mr2J7ZcQ10dchOciShqx4Ufc3gz5m5tr/NJRk+qjJsQ6UdBTQM3SOgIu8IhrAb21CufVMufl'
    b'gJbv0bKWLkpHYjoS0jc9QhMSmQGRCYkkxEmMkRinhk5/DxeX8KSMMQYkAYuMgyX9SHaeTJeO'
    b'oI6aPJJcNzl5zRyBxiOsbNMVj7B3josHqItRF6Eu5l03YN/2+EfbjhcOW0g0x/RaVVI9Q1wv'
    b'0V6vcrJW5bhc4tQzXBjoSETPdOmaPn3bJzYDkAhnonRoJhkHQbFp1VYsKkJkfIzxR5KYSusQ'
    b'aKZjMpNKBNE0hDi19jOfNUkchSUchCx9YbB+FVVH3L9AJQLjoRoTOZ9ThIFejHIwRRPbKlCt'
    b'EDUqHG+tca9e5TgIGHhKy/Rp2y4Dr0douqiJEoDi0ghbbvbPJSeHVUkKRjzEesmklA53JNWd'
    b'WdAbxnNjkk/jZMUXPKgsjG5J2lnpcDEe1q8iCHHYQeMI1GAQKuLhRzoH3pJQBVy1xOm1Bn/Z'
    b'WON9G9DzYmzpnIHfIrY9nAySgJ7AcK2BLig3vcSQGQr54Z7mv1LdmUnlWOApb2aNnZt4xLQj'
    b'Fke3sovFIClc41dADHHYhThEgDKGknOIK8hDzSx84ksjhJs17t3Y4s/8KocW/EoLyqf0TQeI'
    b'yC8e0Vn9OGcIKopIRCCOi2ySyqDmpLEYar6KIknNmVtzqYqkoTCDGJO4cWrBgEnvjEmSF1VV'
    b'gtglUficE7IK1N61Bt+9vs03TIUw6BPUDnFeC2UwUwKXPfJ5Dk9CKoSjCLXIGDdhtg5NipiG'
    b'qhN6d3GsIHPhyHrVpA9pwPiIdYiLqapScm70AKtAFRjs1Hnrxg7/mwq20savPsbZdrqO4elc'
    b'5nEnTAlkQI3e9EWFGxKmh/tUDQX3zV/OMXZjpsAzyIkiN8Yi1sMDrHOLgRY8eLRe5Qc3dvhf'
    b'1HCVLn71IWov5kJdVgVowQmRAQ25oERuLdgSUEWKh39RAnIh2IzFSPplBDdXjBVB5q5gnvFd'
    b'4HFwY5M/sWt0gphy9TFqO8MUz5VCTQ/HgJo5p6xRQQp/EdS8zpCCu5Jz08s4dfwzF/qw8XOW'
    b'6ywoqL9d4/9W1/lAArYqR2AvVoe6yqEKEhGYMyr0hlPBeIK0GGrRNWMOYY6BmYS5dPvGgCox'
    b'BTp90Rr8wONgq8G3tErN72P9U4R4dajLSuvQxlWcabFLJxll+YefYfyvAnUIdnmSMgyLTX7V'
    b'w+AyH3rRTpH0q7hW4kelGo8IqAdNjOnPHJpXBTX5XlHpUZfWqEH5QZd3U5c4pqyIxQ5CvpEy'
    b'7hfnfxXhQiwDYxZLae6+fq3EPVPGCAS2TWK8fbRQh60Xh6Wf5Kmyczp11RSDSQmehppcUyix'
    b'yrjemashNDGWL7D0rU3Xji6mI0bolHweEGAlIjADitZrPzXUiUNEUC0R9Tc4DmsLoc47Vww1'
    b'Obyl4M2oJh+Tv8DS8X205CH9aPHTitDxPY7xsKYPMp7Vnd+Zl+uAxAMO6Heu89P+LQ6CXVTM'
    b'CFCBLatIgcMwHypkk9eKUEe1jkyQDpYTG6CBN2rkvIIFBmLpi6WEw475RlcPdfjwcYkn4U3u'
    b'e9eJvPK4GTUFddYm5vlQF6/3nqhk2iwZNaiP5YktEZX8JXoqXZuQqixfDZ7a+X0xY0JcTVUY'
    b'JK5wZhpgAySLag2lcr5DkAQg50PN9PDyVsHUkYXVkgZ0sexLiX61lGQ753YP4CCIYjyESH2c'
    b'82aJx5WYXyICcUB7sEOLGmKTOGySTjHTdc+JuS5zjbmUcs39kWUtQzHc1xLNagVK/myguYev'
    b'RhGbOC6cj4uqGC3o5yuAmpy26GCb/fgZul5pJK1DHTvfo1ocH7isHTtRw5iPLYIRwwElHpWq'
    b'uGqwEIE6pdbtc4sBp/i0ww1wuQ65jPc1zz2NK5wNbnBgNzBpYlCGKZl5UCeGv7CUNK/oIBS1'
    b'PwnGiBiOpMQ9W6G3Xk3VwXybttzu8UrcwTOGD8NNZLCRDM258dRVoZJMjVGdB2wTmSDJGGCz'
    b'pPUITCHURQin9bLIArBTrm4+fjlWbgI2FI/3qHJar6KlGb5HTiuYdp+XL5p8ygw4oMrj7nUk'
    b'rI+yoMW3rQQ1a2TH1WmZKhiLYpJdNTj8oedVALVwtp6dQZAiO3bpNk49VBKnVZKFDB/EVT4o'
    b'17nWqOB3citlisoNHTtPTviNtQ0eenu8H+7iXfTZWttHvPZwj8MCqy19oGT3y9B6ybngnqvS'
    b'jrYZGJ9NibklA57VAQ0c7+ka3zfraWahIII1A+IiC2LF7UhFibR0MEmyyKEpJd62dT65WWfz'
    b'5CJZdzrnsM0On3zymN98psR/9Tf5QfgML50LO7VH2KAFRMVok7WTqCsR9eu4sIa4AKcGRRmI'
    b'o48jxBDG6zTtNq95Xd50F7zabbLTa3NRrdCr3OKvZI0wDeiP9h4Mia0MdQh2mUMLfh+LcIkg'
    b'YomNz7tRnXv1Bp9unGGOLuYnEiOl/vCEL/oeXBP+p7/Oe+GzXD+v8FzpgGq5CV4PkZhsUQRo'
    b'kthwJboXe/y4+wxPqKT5oqw9mYFvec4Tvux1+Wz3mFvHh1SOW0jsKD27zU75Gr5GhDqaxFYZ'
    b'tbOC3ysEYSb03FiaO5nAVAzGWB5Lhe+YNV7aWWej1UvWeRVBzY5+xPrPDvkSsL4b8SelDf5y'
    b'sMtJr8aNXpMbpXN8v4Xx+ngmAhOjCHF/g/3wFo+DrXSWl1FbSKanOzLgK3rMmycHbD08xDZH'
    b'G0rseo+13R6+CVH1EZnYlVgQl81bCLOgFmZpizqreJnAuBLXYabT4mzAn7sGr621eH2ng/+w'
    b'OVrbNUMcpBey/uEBf6vb5/qNLt8sbfGNuMZPoho/7W2z3e2xbnqUTB9rBjiEc7fFI7uFSb2o'
    b'xHRKO1odn6DDb7snvPb4AfUHR5Ctjswmzyhiw/Wou5CmcajKKDki84f7bKjJsXBb/TROGeXx'
    b'JQslpuiNgFrEeRyYKv9HG9zc7XGz08ecdBaHFPsxpQcnvHjRZW+vxSc2t7lbWuctr8LjuMZ9'
    b'TVY+erEixuC8ALFBKq0jD8pTxyfo8VvRIb9y8ID6z54UjhqvF7IZ9rge9LjvaqgxqVYbF5pV'
    b'ocIldGxmghR5Iol7qGAssQ14K17ndqnHl2+EbAxipNWbXXB2xIo96bB+0ef19SYf39ngS+ub'
    b'vOuv8x4VjvFoqyUUixOLM4KTJD1vESrE/DLn/O3wMXeePKKyfzQONVefaffZ7HZ5odLiu7JB'
    b'qF7S/plLeWacvvTkNQtmHqomQYpEag3iPJq2xp9GG2zUIz77bMzaz3LDsQhq/uhHmMMWG6cd'
    b'GvVj7qzXOG+scVKpcuyXaZmAvhgGmrz0wcaJXbod9rjdPmH7+AT/8DzZ6DyrvkHM+uk5r66f'
    b'8bbZ4cf4qYMCI50wH+AsL2yp7UjTweDZKYthUMN4GOvY13W+GsawDp99Dur3j5GL/nLrDhQI'
    b'Y8xph3KzQ9k7YbfkoYGHK3k4z0NtOmGpYsII2wuTPbm9iT1lRfXFjuDwjDsbR3xxp8GxljlV'
    b'S7In0U5MI8tkafM6dsUkYjGIrOFZxCtZLSPqgQ34UDf5z5HQb8DnnxM2H54g573lN9PlIEsY'
    b'I9pPEhX5FSxDN7HgvjmHtEM2Hh7xhaDM+XqJP5UbtKSUc2ZnqYT5tq198df/+d81XuXTcysf'
    b'bu7Iv1RW03VU+VxCbs2B5BogQpOAe7FlEBi21zxqotgwHr3cYZUj/wwuheomvrcGvNQ2XdCB'
    b'pjegFg24UY7xA8uxlLmQdOV2foVhavnolMs9EbeNem+vBlYnwOZdhbTyBK6SBY81bZCI0DYB'
    b'Hzifx0YorQXUaz6+lwxjcbnyZgnLRDIyoQJiDZQ8tF4i3qjR32nQutbgdKfBYLOKrfhYVSR2'
    b'MyCD6YbUBj1uBgM2A6VjfM7FJ8pe1ZOtlZ0CWxBijPpvX+59BcLEIoKR1I5Fi4wZmcoiWDF0'
    b'jeHPQp8PojKv18u8Xl/j+UGP9U6PcqeP1x0kwz0q2NcgMr5Zo+QTlnx6JZ9uEHAaBDy2PvtY'
    b'9tXjxFmumZg3Nvu8cq3Lzuk5peOLZLdPOOFqxw77pMVuP+RLN7vc3G1xt/wM37E7PKJCnCyk'
    b'n4pHT7OR5dLfSxCeEqZkCKXuvDEgHuIk3f4gON/w0AQchlW+49q84Pe4vRlyYzNiWyPWYkfJ'
    b'xfguWxmdvJs5FEPfGHpiaIuhaSynWI5Idrwc4NPSgAvx6RsPrMFqzLtxl096bd7cq/LxrS67'
    b'rTaVsw6m1UN6YbK0XxWcIs0u9f5jXm332Ntr8VLjjG/7e7xrtjgjSNY9FFkMGdT0eCqwUxne'
    b'3BadoZ7VZDJTM8orWbFpXMHjUVzhwIXcjQf4LqRBxLrEeJ7DVx2GdR0QIoRq6GNoYumpR2ws'
    b'TjzU+LjUUTAi2Cz/r8pjW+WJW+OduM1LtsOnturc2exzvd+n0e1RvugNRwpOUXX4zQv2UNb7'
    b'XZ7ZbvNScM5ds8f7ZpN+oYw9jYOQriHQ4TvTR3mvkQc2KdGSBk4MYpK4rYrDGIM6izEezgXg'
    b'lRmo41CVJ+qyyqZGQuaIiDHDZe2SLiA2mZcko/Yl2/0VNODEVbgbD/h+3GXXdXip1Of58oC9'
    b'jYhNF9FwMeU4JnAOq8nah8jz8N2A56ITnER0xONHZntCI0xbCEu90CyZq2QYcVeR4d/5Z06A'
    b'K6PIe24WkhSSJN6ZqAVxqHUYFyc7rXV8H0FxX8kwEK5Dby+ZVIb7BSSDmk28mgKOURtw4Sq0'
    b'tMGHcYiN+9Q1pCExVRtT8RxVlECykWZxzhJGPuemymPnQV4dTKW+UwdhGTvWpQZ/AtYky3KM'
    b'I9msm6ayVRn7HxOGjEdws5DfcB+q0bSs5CcpgOFrUHKjRYaFph2bPpSORbRkmM4e3ZurT2Oy'
    b'9wmgDuccsTpO1HGc29me9F86KiTN5hof4wVJwCc3eoqgwtKqQEg2d2SvUIrBSbI3PzWThjbu'
    b'8PkLlHxmSUi6pmBoCzPsHHGO6akwX46k906+7W1cBYzfm8HNVIxDXCIcktWbz8Pk0k3DvRfW'
    b'y61DYC7UFcBmd5tkpXz65g4UxDjUuXR4am4o55btFOjeUa/npVLBjumfMTzZA00vrpCJTpxI'
    b'DqajSbApxGSUSM4mL3rVVX7fV6bHM7UzD6osA3Y6ipXATTyd9AUehuHb07I3Y47rl3xUfNrK'
    b'n0ylS274TmdKZXokLFpMMdxVqOkWJjNqSQo0X8to62bWQaOdNTJ3d83oGUZvk19EeCZczcHN'
    b'VEIO5hByXpoUnQsj1Z9FIbWnWqGSjhOTvfhU0alFIjqmemRskpLFUNPDK4pbLAt3FADJJo5s'
    b'OOXjjBOpZV0ElWHHCJK+wEbHrhkpiFWgZl9PBrGL7pm+b5FOzX+vqnguDgeLXzM7xmUMbn5U'
    b'juTS5YRUIDfbTkKebtR4o2U4WeWYXwnU5e5ZFSqAc9HADLrNR+rigmzf+PPPNMuyLedpzmmk'
    b'7HMzdDrhZP/GGpTLjE5CHV2WmFD/P0BVF4eDTvOhObv/9vfisLufLXIo+iw8MpvP5Leh57ZT'
    b'ZropHwEjcTJQyVlpxQ82jJBNdsxfM6ggxGF3//z+29+z3ZOfRJsv/tr1oLL5mpiZ6y+XgDva'
    b'OZ38Tg5krvEyEQGDmcAmt1HmO+evI1SNB3H3+IP/8uOv/Ys/soPWo5IY72Ht2ssv2KD2vBjv'
    b'6eAOJXTaTM/czHE7U6aA6ZRXI+OfbMIpvOYpoRaUOx9qUq+L+tpr7n99/5t/+G9P3v/aYwsE'
    b'5/vfbmO8H5bqe4F4/g1EKuMey4qf1LtRl7iOmr3EN/V8lMytnHBxcVNu7+yPm/u9MKtdy7Q9'
    b'V87M7x24GBf3iHtnx53DH/7R/W//+z98+O1/9yOgK0AdqAD1jdtf3Lvxxj/4zNreK6975cYL'
    b'GK86wxZZcKSgXDz0/4fuJNn/bZMGWvJO2pxQZ1bseHO0+JJMxvJ+SZF0FkmizvheJq4RVXVR'
    b'O+qef3Bx8IO3Hr/9H++e7999AlwA3f8HzItcIhZeKSMAABeIZVhJZklJKgAIAAAACAAAAQQA'
    b'AQAAAIAAAAABAQQAAQAAAH8AAAACAQMAAwAAAG4AAAAaAQUAAQAAAHQAAAAbAQUAAQAAAHwA'
    b'AAAoAQMAAQAAAAIAAAAxAQIADAAAAIQAAAAyAQIAFAAAAJAAAACkAAAACAAIAAgALAEAAAEA'
    b'AAAsAQAAAQAAAEdJTVAgMi4xMC40ADIwMTg6MDc6MjkgMTc6MjM6MjIACAAAAQQAAQAAAAAB'
    b'AAABAQQAAQAAAP4AAAACAQMAAwAAAAoBAAADAQMAAQAAAAYAAAAGAQMAAQAAAAYAAAAVAQMA'
    b'AQAAAAMAAAABAgQAAQAAABABAAACAgQAAQAAAHcWAAAAAAAACAAIAAgA/9j/4AAQSkZJRgAB'
    b'AQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIs'
    b'IxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIy'
    b'MjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAD+AQADASIAAhEB'
    b'AxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA'
    b'AAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0'
    b'NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZ'
    b'mqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3'
    b'+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQA'
    b'AQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygp'
    b'KjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaX'
    b'mJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3'
    b'+Pn6/9oADAMBAAIRAxEAPwDxHQ9GuNd1KOzt+GbOW44wCe5HpXsuheFdL8OxqYk867/jnyy7'
    b'uuPlyQODiqPgXSF0jw8kjw+XeXOfP+bOdrtt7kdD2rpK+jy/AxhBVJrV/geTisS5ScI7E/2l'
    b'+3FJ9qk9agor1eSPY4uZk/2qT1o+1SetQUUcsewczJjdSetH2qT1qCijlj2DmZP9qk9aT7VJ'
    b'61DQaOSPYOZk32p6PtUnrUFFPkj2FzMn+1SetJ9qk9ahpKOSPYOZk/2qT1o+1SetQUU+SPYO'
    b'Zk32qT1o+1SetQUUckewczJ/tUnrR9qk9agoo5I9hczJ/tUnrSfapPWoaSjkj2DmZP8AapPW'
    b'j7VJ61BRRyR7BzMm+1SetH2qT1qCinyx7BzMn+1SetJ9qk9ahpKOSPYOZk/2qT1oF0/fmoDS'
    b'UckewczMvXPDGmeIY2MieTd8bJss23pn5cgHgYrx7WNKn0bUpbK4+/HjJ47gHsT617rXO+Od'
    b'LTVPD7zCLzLu2x5J3YxudQ3cDoO9eTmOAjODqQVmvxO3CYqUZKEtmdNb48hcdOf51JUVt/x7'
    b'p+P86lr04/CjkluFFFFUIKDRSUAFFFFABSUppKACiiimIQ0UUUAFFFIaYBRRRQIKKKKAA0lF'
    b'FABRRSGgAooooAKSlNJTAQ0UUUCCorkA27A9Dj+dS1Fc/wDHu34fzpT+Fjjuie1/49k/H+dT'
    b'VDa/8eyfj/Opqzj8KLe4UUlIelMSFoqPdRupcw+UkoqPdRuo5g5R9FM3Um6jmCxJSUzfRup8'
    b'wco+io91G+jmDlJKSkRJJPurn8asC0Ycu+PwrGpiqVP4nY6qGAxFf+HBsgozU5W2X7z5/A0n'
    b'nWi9Bn865JZrQW2p6lPhnHz15bEGaM1N9ptv7v6mk860brx+dJZvR7M0lwrjktEiLNFTeXBJ'
    b'9yTB/wB01HJbyx84yPXiumljqNTSMjzcTlGMw+tSDsNpM0zfRurq5jzuUfRTN1G6nzByjiaK'
    b'Zuo3Ucwco6imhqdVJ3JaCorn/j3b8P51LUVz/wAe7fh/OiXwsI7k9r/x7p+P86lqK2/491/H'
    b'+dS1lH4UU9wpD0paQ9KbBETUzNPaojWTNEO3UZqPNGaVxj80ZplJmi4WJN1JupY4pJjhFz+N'
    b'W1githulbLemDWFbFU6K956ndg8txGLlanHTv0IYbaSXkcD1qwRb23X5m/EVBNePJwvC1VNe'
    b'JXzCrU0joj7nL+GsPQSlW96Rbkv5G4X5R+dVmdm6nNNorgbvufSQpQpq0VYKQ0tJQaBSUtJQ'
    b'AVNFcyRHg8elQ0UClFSVmjR2x3iZXh/xqkwKMVbrTUcxsGXrV2ZVu4d6/fH+NetgcdKLVOo9'
    b'D4rP8hjyvEYda9UU80uaj5U4PWlzXvJ3PhGraMdk0ZpuaKdxDwacDUWacDWkWQyaorn/AI92'
    b'/D+dOBplz/x7t+H86cvhYluWLb/j3X8f51LUNt/x7r+P86lzWcfhRT3FpDRSGqewIiaozUjV'
    b'Eck4rFmiGk0KCxwoyauRWXG+Y7V9Ov8AKntdxwjbAv45/wAa86vmFOnpHVnvYDIMTivea5Y+'
    b'ZFHYSMMudo/OpNlrByfnb8RVaSZ5D8xz+FR15dXH1qnWyPrsJw3hKFnNcz8y3JfORtQbR+dV'
    b'SSTk0lFcTberPfp0oU1ywVhDRRRQaBRRRQAlFFJQMKKKKACiiigAp8UrRNlTTKSgGk1Zl4Xy'
    b'sP3kefxo8yzk+8uD9TVA0VrCvVh8MmcFbKsHW+OCL5tIZP8AVyY/4Cahks5Y+QMj8KrdKt2k'
    b'0vmhQcj04rspZnWj8Wp4mL4Vws4uVJ8rK1KDUt4y/aSF/H8qhFfR0p88FLufnWIpeyqyhe9m'
    b'SA0y4P7hvw/nSio7g/uG/D+daN+6zJbly2/491/H+dS1Fbf8e6/j/OpaUfhQPcKQ9KWhUMjb'
    b'RRJpK7HCLlJRW5EI2lfaoqx+6sx/ek/Ef561NIjQRbIl59c1nNFKTlh+or5rGY+VRuENEfoW'
    b'S5BTpJVsRrLt2CWZ5myxqOlII60leafXJJKyCiiigYUlFFAwooooAKSiigYUlFFABRRT1idu'
    b'i/rQJtLcZRVgWcx6rj8RTvsePvSY/Cmk2ZSxNGHxSRUoq6LaEfx5/A1We9somKhNxHuRWkaN'
    b'SeyOOtm+Eoq8pkXWpUt5X+6v6io21ZhxFBgeu/8A+tUMl/dy/wDLTaPTaD/SumGX1pb6HlV+'
    b'KsLD+GmzQ+yLGN0z7R6Yz/KoZNQRV8u1H/Av/wBYrNKlzluTUqriu+hlsIu89T5zH8SYnEJw'
    b'h7qJFyevWpQaYBTq9iKsj5eTux1Rzn9w34fzp+ajuP8AUN+H86qXwslbl+2/491/H+dS1Dbf'
    b'8e6/j/OpacfhQPcCaYzOq/I20/TNPNMYcUpxUlZjhJxknF6lV7+7Q43/AKCm/wBrXS98/l/h'
    b'T5Yw1VHj2nmvOnhKX8p6UMwxK2my9FqyyttniwPXd/gKluYREwKn5T0rJCZcCtm94WMfX+le'
    b'TjqEKVnHqfYcN5hiMROUKrukVM0UUV559gFFFFABSUUqqXbCjJoDYSlVGkOFGanKRW+POOWP'
    b'8PP9Kd58h4x5Y/u8HP41pGm2rvRHlYrOKFB8q1Yi2ZH+sbb+GakEUCdt/wCJFRF2P+z+tMOD'
    b'1GaTlTXmeJWz2tL4NCyZ0T7o2/rTWuXPQ5qCip9rbZHm1MdXnvIeZSeoxTd7f3v0ptFS6031'
    b'Od1Jvdilm9azWXc5NaPY1T24Y17GUty5rnnY6T5URiOnBKlApcV7SieZcYEpwWnUVSRIUtFJ'
    b'VolhUdwf3Dfh/OpKjuP9Q34fzpy2YluX7b/j3X8f51LUVt/x7r+P86lpx+FA9wpD0pc0hpvY'
    b'S3IWFQuuanaomrFo1RXRf3yitO/++o+v9Kox/wCuX8f5Ve1D/Wj/AD6V4OafFFH23CK1mynR'
    b'RSZryj7kWkoooGORDIwVepqeSUQHyYOZD1P696SST7Fa7h/rX6D6H/69Qwx+WnJyx6n1rohB'
    b'Qh7SfyPlc5zR87w9J+rHIgTLZyx6t607PbtQTmkrlqVJTd2fNhRRRUCCiikoAKKKKAA9DVaQ'
    b'YmYVZ71FOOEPc5zXrZTO1Rx7nLjIXp37DBS0gpa+jR44UtJS0wCkpTRVIhhUVx/qG/D+dS1F'
    b'cf6hvw/nRL4WC3L1t/x7r+P86lqK2/491/H+dS04/ChPcKDRSGmwW5E1RtUjVG1ZM0RGpxKp'
    b'q/qH+tH+fSs1jg5rSvhkI31/pXhZqtYs+14Rn+8nEpUUUma8g+8FqS3TzJgtRVasuHZvSmlf'
    b'QyrT5KcpdkVriTz9RJ/hTp+IqY8cVUtTueRj7Varox3uyVNdEfmcZuo3UfVthRRRXCUFFFJQ'
    b'AUUUUAFFFJQAUkozEx9MUuQBzVdrjzAVXkHqa78upzdZSitEZYiUY03zAtOpop1fVI8IKWii'
    b'mAUUUVaIYVFcf6hvw/nUtR3P+ob8P50pbMFuXbb/AI91/H+dS1Fbf8e6/j/OpacfhQnuFIaW'
    b'kNNgtyJqjbpUjVGayZoiCStFz5tgrDtn+dZ7irunnzLd4fTH8ya8vM4c1K/Y+i4bxHssYk+p'
    b'VopSMHBpK+fP08Ks2nRx64qtVizbE4B7/wCFOLs0zDFRc6MorsypZY2ye2P61Zqov7i7aM8A'
    b'9fyq3711ZjH94p9GfmVHSHL1V1+IUUZpK881CiiigAoopKACiij6daEruwyOdgIj+lVkFLI2'
    b'+Tj7o6U9RX1WBoeypJPc8jF1VOdl0HAU6kFLXoHGFFFFAgoopatEsKiuP9Q34fzqWorj/UN+'
    b'H86JfCwW5ctv+Pdfx/nU2ahtv+Pdfx/nUtOPwoT3DNIaWkNN7AtyNqjNSNURrFmiGNS2cvk3'
    b'Snsev5UGoJBWNWCnFxfU3oVXSqKcehfvI/LmPoar1cVvtdmG/jX/ABqnXydSDhJxfQ/X8DiY'
    b'4mhGpHqFKrFGDDqKSkzUnYTajb+cguE79f0FQW9x5g2t97+dWba48o7W5Q9ajvNO/wCWsPI9'
    b'P/1mvRpThXp+xqbrZnwecZZUwtZ4iirxe6HUVSjuyhxJx/tVbV1dcjpXDWwtSk9UeTCpGavE'
    b'dRR16UhOO+DWCTbsihcGkrPkuJWb9220fQGk824/56f+OivTjldRq7ZzvF0k7amjketNdgqb'
    b's9Kob5j1k/QVftdPaTDzngdv/wBRq1gFRanUloiqNSWIlyUYtsrQxPJwgz+NXlsZduW4/Kpn'
    b'u0hG2JenfNSWlyZmKtW0s0fNaC0PYp8KuNJ1Kz17GZ0NLSy8SsKbXuRd0mfGTjyycewGlpKW'
    b'qJAUtFFWiGFR3H+ob8P51LUdx/qG/D+dKXwsa3LVt/x7r+P86lqK2/491/H+dS04/ChPcKQ0'
    b'uaQ03sC3IzURqRqjPWsmWhpqNhUpphFQykLZXH2efB+63X8jVu7h2Hev3TWa61esr0EeRN+B'
    b'/M9q8fMMK5fvIn1fD2brDy9jUej2IKKsXFsYTkfdqtXin6JGSkroWpoLl4TjqvpUFFMcoqSt'
    b'JF6S3t70ZU7X/E/56Vmz6dNbtuA49cj/ABqQHByKsx3ssfGcj8K7KONnBcstUfN47huhXfPS'
    b'fLIyxNOP+Wn/AI6KUySuMM+Qe2BWx9rhk/1kfP8AvGj/AENu2PzrqjjMPe7jZng1eHcwjopX'
    b'RkBKcErW22f+c0Ce2iOUXJ+prd5nRS0TOaHDGNlKzskR2liEHmy8egplzdGU7V4Wknu3m46C'
    b'q9eRXxEq0ryPt8rymlgadlv3CrNg+2cD1/wNVaVGKMGHUVgepOPPFx7k14myfPr/AIVEK0bi'
    b'MXUAkT73/wBes0ccV9TgayqUl3R+Q5vhJ4bEyTWjHUtJSiu48oKWiiqRLCo7j/UN+H86lqK4'
    b'/wBQ34fzpS+Fgtyzbf8AHuv4/wA6lqK2/wCPdfx/nUtOPwoHuFIaWkNNgtyNqYetPbrTDWTL'
    b'Q002nGm0hjWFQOlWKaVqGikyS11AxDy5+U9f/wBQq09qHG+E5Hp/+usxlpscktu2Y2wPTAry'
    b'8Tl6m+aGjPpMr4hq4W0KmsS2yMhwwxTalTVgRieP9f8AAVILrT5e+D/wKvKnha0N0fY0OIMH'
    b'VXxWK1FWttmek3/jppdlp/z2/wDHTWXsp9jtWZ4R/bRUoqzmyXrJn/gLUw3lgnQ5P/AqpUKj'
    b'2iZTznBQ3miDrUiwSN0X9acdVjUfuos/8CP+FQvqty/3Rs/I/wBK3hgK0uljzq/FGEp/DqWR'
    b'YzEfdx+IqKSCSP7y4/GqTTXDnLS5P+6KtwapJH8sw3L65x/IVrPLqsVdanLQ4spTnyzjZDKK'
    b'vAWt2N0bYP0NRyWMi9Pm/IVwShKLtJH0tDG0K6vCQ22uTC3P3atTWqTjzIuves9kZeoxT4Z3'
    b'gbI/KtKGInRlzRObMsro46naW40qUOGGDSitJWhu0+Yc/jVWayeI5HIr6LDY+nW0ejPzbMMk'
    b'xGDk3a6IKWkFLXoo8R7hUVx/qG/D+dS1Fcf6hvw/nSl8LCO5Ztv+Pdfx/nUtQ23/AB7r+P8A'
    b'OpacfhQPcWkJooqrCIzUZqYioyKhxKUhlJTiKbip5R8wlIRTqSiwXGkUwpUtGKTiPmKzR0wx'
    b'1b200rUuA+cqeUKPKHpVrZRspezQ+crCIelOEdWNtG0U/Zi5yER0oSpttLimoC5yHZTTHVjF'
    b'BWnyBzFMx4bcOtTxXtxD/FuH0Ap5SmFKyqYeE/iRtSxVWk7wlYsrq7EfvIv/AB7/AOtUg1S3'
    b'P3o8fif8KoeXR5dckstovoenTz/GwVlI0l1K0HQfz/wqQ6rAU2r/AF/wrKCVIq0RyyinfUqp'
    b'xDjKitJosSSrK24Lj1OetNpqinV6UIqEVFHh1ajqTc3uwqO4/wBQ34fzqWorj/UN+H86cvhZ'
    b'K3JrY/6Ov4/zqbNUdJulu9OimQ5Bz/MirtODTimglo2goooqiQpCKWiiwERFNNSkUwipaHcj'
    b'pMU8im0ihKKWigBKWikoAKSloxQAUUUUCCiilpgFFFFABRilooATbSbafRQK43bS7aWigApa'
    b'KKYBUdx/x7t+H86lqlq10lpp0sznAGP5gVM2lFtjirtI4zwH4gjiQaXMdpH+r77vvMeg4/Ov'
    b'RAQRkV8+qxVgynBFdvoHjS8yltPH5rHOZNwX1PQLXh5dmSjFUqvyPSxeEbbnA9MorJj1ZmXJ'
    b'j/8AHv8A61P/ALUb/nl/49/9avc9tA872cjTorM/tRv+eX/j3/1qP7Ub/nl/49/9aj2sO4ck'
    b'jTppFZ39qN/zy/8AHv8A61H9qN/zy/8AHv8A61HtYBySLxFNIqidTP8Azz/8e/8ArUw6kf8A'
    b'nn/49/8AWqXUgNQkXzRWf/aR/wCef/j3/wBak/tI/wDPP/x7/wCtS9rEfJI0KKz/AO0j/wA8'
    b'/wDx7/61H9pH/nn/AOPf/Wo9rEOSRo0Vnf2kf+ef/j3/ANaj+0j/AM8//Hv/AK1HtYi5JGjS'
    b'Vn/2kf8Ann/49/8AWo/tI/8APP8A8e/+tR7WIckjRorO/tI/88//AB7/AOtR/aR/55/+Pf8A'
    b'1qPawDkkaNLWd/aR/wCef/j3/wBaj+0j/wA8/wDx7/61HtYBySNGlrN/tNv+ef8A49/9aj+0'
    b'm/55/wDj3/1qPaw7hySNKis7+0m/55/+Pf8A1qP7SP8Azz/8e/8ArU/aw7i5JGjS1m/2mf8A'
    b'nn/49/8AWo/tNv8Ann/49/8AWo9rAOSRpUtZn9pt/wA8/wDx7/61Nk1ZlXIj/wDHv/rUe1gP'
    b'2cjUJAGTXnvjnxBHMraZCdx/5adtv3WHUc/gag17xneFntoY/KYYw+4N6HoVriySxyeteJmG'
    b'YqUXSpfM9HC4Rp88z//ZAM+aBbIAAAAldEVYdGRhdGU6Y3JlYXRlADIwMTgtMDctMzBUMjI6'
    b'Mjg6NTAtMDM6MDCcG2NEAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDE4LTA3LTMwVDIyOjI4OjUw'
    b'LTAzOjAw7Ubb+AAAABp0RVh0ZXhpZjpCaXRzUGVyU2FtcGxlADgsIDgsIDgS7T4nAAAAIXRF'
    b'WHRleGlmOkRhdGVUaW1lADIwMTg6MDc6MjkgMTc6MjM6MjLZyDOwAAAAFHRFWHRleGlmOklt'
    b'YWdlTGVuZ3RoADEyN9HL3iQAAAATdEVYdGV4aWY6SW1hZ2VXaWR0aAAxMjiSCNM4AAAAGXRF'
    b'WHRleGlmOlNvZnR3YXJlAEdJTVAgMi4xMC40QDoIZgAAAABJRU5ErkJggg==')

class RenewTask(Process):
    def __init__(self, queue, user_id, user_password):
        Process.__init__(self)

        self.queue = queue
        self.user_id = user_id
        self.user_password = user_password

    def run(self):
        renewed = renew_books(self.user_id, self.user_password,
                              status_callback=self.OnNewStatus)
        self.queue.put(renewed)

    def OnNewStatus(self, status, progress):
        self.queue.put({'status': status, 'progress': progress})

class StatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-1, -1])

        self.SetStatusText(utils.get_module_version('minervaboto'), 0)

        self.gauge = wx.Gauge(self, -1, 100, size=(158, -1))
        self.OnResize(None)
        self.gauge.Show(False)

        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, event):
        field_rect = self.GetFieldRect(1)
        gauge_rect = self.gauge.GetRect()

        width_diff = field_rect.width - gauge_rect.width
        field_rect.width = gauge_rect.width
        field_rect.x += width_diff - 3

        field_rect.height = 14
        field_rect.y = 5

        self.gauge.SetRect(field_rect)

class LoginWindow(wx.Frame):
    def __init__(self, title, user_id='', user_pass='',
                 config=None, config_file=None, has_config=False):
        wx.Frame.__init__(
            self, None, -1, title,
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX
        )

        self.config = config
        self.config_file = config_file
        self.has_config = has_config
        self.process = None
        self.queue = Queue()

        self.panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 5)

        logo = wx.StaticBitmap(self.panel, -1, __LOGO__.GetBitmap())
        sizer.Add(logo, pos=(0, 0), span=(1, 5), border=20,
                  flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)

        label_id = wx.StaticText(self.panel, label='ID/CPF')
        sizer.Add(label_id, pos=(1, 0),
                  flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=10)

        self.input_id = wx.TextCtrl(self.panel, value=user_id)
        self.Bind(wx.EVT_TEXT, self.OnInputChange, self.input_id)
        sizer.Add(self.input_id, pos=(1, 1), span=(1, 4),
                  flag=wx.RIGHT | wx.EXPAND, border=10)

        label_pass = wx.StaticText(self.panel, label='Senha')
        sizer.Add(label_pass, pos=(2, 0),
                  flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=10)

        self.input_pass = wx.TextCtrl(self.panel, value=user_pass,
                                      style=wx.TE_PASSWORD)
        self.Bind(wx.EVT_TEXT, self.OnInputChange, self.input_pass)
        sizer.Add(self.input_pass, pos=(2, 1), span=(1, 4),
                  flag=wx.RIGHT | wx.EXPAND, border=10)

        self.check_save = wx.CheckBox(self.panel, label='Salvar dados')
        self.check_save.SetValue(has_config)
        sizer.Add(self.check_save, pos=(3, 1), span=(1,1))

        self.button_renew = wx.Button(self.panel, label='Renovar')
        self.Bind(wx.EVT_BUTTON, self.OnRenewClick, self.button_renew)
        self.button_renew.SetDefault()
        sizer.Add(self.button_renew, pos=(4, 4), span=(1, 1),
                  flag=wx.BOTTOM | wx.RIGHT | wx.ALIGN_RIGHT, border=10)
        self.OnInputChange(None)

        sizer.AddGrowableCol(2)

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel.Sizer.Add(sizer, flag=wx.CENTER | wx.BOTTOM | wx.EXPAND,
                             border=30 if wx.Platform == '__WXMSW__' else 0)
        vbox.Add(self.panel, flag=wx.CENTER)
        self.SetSizer(vbox)
        self.panel.Sizer.Fit(self)

        self.status = StatusBar(self)
        self.SetStatusBar(self.status)

        self.Show(True)
        self.Bind(wx.EVT_CLOSE, self.OnWindowClose)

    def OnInputChange(self, event):
        if (self.input_id.GetValue().isdigit() and
            len(self.input_pass.GetValue()) > 0):
            self.button_renew.Enable()
        else:
            self.button_renew.Disable()

    def OnRenewClick(self, event):
        for child in self.panel.GetChildren():
            if not isinstance(child, wx.StaticBitmap):
                child.Disable()
        self.status.gauge.Show(True)

        self.process = RenewTask(self.queue, self.input_id.GetValue(),
                                 self.input_pass.GetValue())
        self.process.start()
        self.OnTimer()

    def OnTimer(self):
        if self.queue.empty():
            wx.CallLater(15, self.OnTimer)
            return

        result = self.queue.get(0)
        if 'status' in result:
            self.SetStatusText(result['status'], 0)
            self.status.gauge.SetValue(result['progress'])
            wx.CallLater(15, self.OnTimer)
            return

        self.FinishedRenewal(result)

    def OnWindowClose(self, event):
        if self.process: self.process.terminate()
        event.Skip()

    def FinishedRenewal(self, renewed):
        for child in self.panel.GetChildren():
            if not isinstance(child, wx.StaticBitmap):
                child.Enable()
        self.status.gauge.Show(False)
        self.status.gauge.SetValue(0)
        self.SetStatusText(utils.get_module_version('minervaboto'), 0)

        if renewed['result']:
            result_list = renewed_to_string(renewed, True)
            dialog = wx.lib.dialogs.ScrolledMessageDialog(
                self, result_list[0], result_list[1], size=(480, 300)
            )
        else:
            if renewed['response']['code'] == 200:
                icon = wx.ICON_INFORMATION
            else:
                icon = wx.ICON_ERROR
            dialog = wx.MessageDialog(self, renewed['response']['message'],
                                      'Renovação', wx.OK | wx.CENTRE | icon)

        dialog.CenterOnParent(wx.BOTH)
        dialog.ShowModal()
        dialog.Destroy()

        if renewed['response']['code'] != 401:
            self.SaveCredentials()

        self.input_id.SetFocus()

    def SaveCredentials(self):
        if self.check_save.GetValue():
            self.config['LOGIN']['MINERVA_ID'] = self.input_id.GetValue()
            self.config['LOGIN']['MINERVA_PASS'] = self.input_pass.GetValue()
        else:
            self.config['LOGIN']['MINERVA_ID'] = ''
            self.config['LOGIN']['MINERVA_PASS'] = ''

        if self.has_config or self.check_save.GetValue():
            utils.write_config_file(self.config, self.config_file)

if __name__ == '__main__':
    title = 'Renovação Minerva'

    config_file = utils.get_default_config_file('minervaboto', 'boto.conf')
    config = utils.read_config_file(config_file)
    user_id, user_pass = utils.get_info_from_config(config)
    if (os.path.exists(config_file) and user_id and user_pass):
        has_config = True
    else:
        has_config = False

    app = wx.App(False)
    LoginWindow(title, user_id, user_pass, config, config_file, has_config)
    app.MainLoop()