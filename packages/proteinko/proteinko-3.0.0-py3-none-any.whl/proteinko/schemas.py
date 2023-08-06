import base64


acceptor = b'YW1pbm9fYWNpZCx2YWx1ZQpBLDAuMDAxCkMsMC4wMDEKRCw0CkUsNApGLDAuMDAxCkcsMC4wMDEKSCwyCkksMC4wMDEKSywwLjAwMQpMLDAuMDAxCk0sMC4wMDEKTiwyClAsMC4wMDEKUSwyClIsMC4wMDEKUywyClQsMgpWLDAuMDAxClcsMC4wMDEKWSwx'
donor = b'YW1pbm9fYWNpZCx2YWx1ZQpBLDAuMDAxCkMsMC4wMDEKRCwwLjAwMQpFLDAuMDAxCkYsMC4wMDEKRywwLjAwMQpILDIKSSwwLjAwMQpLLDMKTCwwLjAwMQpNLDAuMDAxCk4sMgpQLDAuMDAxClEsMgpSLDUKUywxClQsMQpWLDAuMDAxClcsMQpZLDE='
pI = b'YW1pbm9fYWNpZCx2YWx1ZQpBLDYuMApSLDEwLjc2Ck4sNS40MQpELDIuNzcKQyw1LjA3CkUsMy4yMgpRLDUuNjUKRyw1Ljk3CkgsNy41OQpJLDYuMDIKTCw1Ljk4CkssOS43NApNLDUuNzQKRiw1LjQ4ClAsNi4zMApTLDUuNjgKVCw1LjYwClcsNS44OQpZLDUuNjYKViw1Ljk2'
volume = b'YW1pbm9fYWNpZCx2YWx1ZQpBLDY3CkMsODYKRCw5MQpFLDEwOQpGLDEzNQpHLDQ4CkgsMTE4CkksMTI0CkssMTM1CkwsMTI0Ck0sMTI0Ck4sOTYKUCw5MApRLDExNApSLDE0OApTLDczClQsOTMKViwxMDUKVywxNjMKWSwxNDE='
hydropathy = b'YW1pbm9fYWNpZCx2YWx1ZQpJLC0wLjgxCkwsLTAuNjkKRiwtMC41OApWLC0wLjUzCk0sLTAuNDQKUCwtMC4zMQpXLC0wLjI0ClQsMC4xMQpRLDAuMTkKQywwLjIyClksMC4yMwpBLDAuMzMKUywwLjMzCk4sMC40MwpSLDEuMDAKRywxLjE0CkgsMS4zNwpFLDEuNjEKSywxLjgxCkQsMi40MQ=='


def encode_schema(fpath):
    """
    Convert file to base64 bytestring. Used for storing in hdf5 files.
    :param fpath: File path
    :return: base64 bytestring
    """
    with open(fpath, 'r') as f:
        bstr = b''
        for c in f.read():
            bstr += c.encode('ascii')
    return base64.b64encode(bstr)
