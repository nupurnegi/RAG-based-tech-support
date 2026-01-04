# def insert_data(vectorstore, questions, answers, batch_size=500):
#     docs = []
#     metadatas = []

#     for q, a in zip(questions, answers):
#         docs.append(q)
#         metadatas.append({"answer": a})

#     for i in range(0, len(docs), batch_size):
#         vectorstore.add_texts(
#             texts=docs[i:i+batch_size],
#             metadatas=metadatas[i:i+batch_size]
#         )   




        