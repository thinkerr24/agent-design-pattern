from openai import OpenAI

client = OpenAI(
    # 指向你本地由插件启动的网关地址
    base_url="http://127.0.0.1:3030/v1", 
    # 此时不需要真正的 OpenAI 密钥，随便填一个字符串即可（但不能为空）
    api_key="any-string-is-ok" 
)

# 调用时，model 填 Copilot 支持的模型，例如 "gpt-4o"
response = client.chat.completions.create(
    model="gpt-5.4", 
    messages=[{"role": "user", "content": "武汉今天明天天气如何？"}]
)

print(response.choices[0].message.content)