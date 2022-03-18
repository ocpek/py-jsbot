def list_header_blocks():
    yield {"type": "header", "text": {"type": "plain_text", "text": "TODO List"}}

    # yield {
    #     "type": "section",
    #     "text": {
    #         "type": "mrkdwn",
    #         "text": "*TODO List*"
    #     }
    # }
    # yield {
    #     "type": "divider"
    # }


def empty_block():
    return {"type": "section", "text": {"type": "mrkdwn", "text": "Empty"}}
