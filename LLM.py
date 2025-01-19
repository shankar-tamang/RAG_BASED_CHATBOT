
# def parse_response(text):
#     # Initialize the output and states
#     html_output = ""
#     in_list = False
#     list_level = 0

#     # Split the text by lines
#     lines = text.split('\n')

#     for line in lines:
#         # Handle bold headers
#         if line.startswith("**") and line.endswith("**"):
#             if in_list:
#                 html_output += "</ul>\n"
#                 in_list = False
#             html_output += f"<h3>{line.strip('**').strip()}</h3>\n"
        
#         # Handle bullet points
#         elif line.startswith("*") and not (line.startswith("**") and line.endswith("**")):
#             # Check if we're already in a list
#             if not in_list:
#                 html_output += "<ul>\n"
#                 in_list = True
#             # Check for nesting (if there are nested lists)
#             if line.count('*') > list_level:
#                 html_output += "<ul>\n"
#                 list_level = line.count('*')
#             elif line.count('*') < list_level:
#                 html_output += "</ul>\n"
#                 list_level = line.count('*')
#             html_output += f"  <li>{line.strip('*').strip()}</li>\n"
        
#         # Handle paragraphs and ensure lists are closed
#         else:
#             if in_list:
#                 html_output += "</ul>\n"
#                 in_list = False
#             html_output += f"<p>{line.strip()}</p>\n"

#     # Close any remaining open lists
#     if in_list:
#         html_output += "</ul>\n"

#     return html_output

# def chat_with_bot(prompt):
#     # Create a chat session
#     chat = model.start_chat(history=[])
#     # Send the message and stream the response
#     response = chat.send_message(prompt, stream=True)
    
#     response_text = ""
#     for chunk in response:
#         if chunk.text:
#             response_text += chunk.text + ' '

#     # Parse the accumulated response into HTML
#     parsed_html = parse_response(response_text)

#     # Yield the parsed HTML content
#     yield parsed_html

