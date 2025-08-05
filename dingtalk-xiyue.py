import requests
import time
import sys

# 预定义颜色映射
COLORS = {
    '1': '#FF0000',  # 红色
    '2': '#FFA500',  # 橙色
    '3': '#FFFF00',  # 黄色
    '4': '#008000',  # 绿色
    '5': '#0000FF',  # 蓝色
    '6': '#800080',  # 紫色
    '7': '#FFFFFF',  # 白色
    '8': '#000000'   # 黑色
}

# 预定义字号映射
FONTS = {
    '最小': '0.8em',
    '小': '1em',
    '中': '1.2em',
    '大': '1.4em',
    '最大': '1.6em'
}

def send_dingtalk_markdown(webhook_urls, payload):
    """
    向多个钉钉机器人发送Markdown消息
    
    参数:
    webhook_urls (list): 钉钉机器人Webhook URL列表
    payload (dict): 消息负载数据
    """
    results = []
    for url in webhook_urls:
        try:
            if 'access_token=' not in url:
                results.append((url, False, "❌ 无效的Webhook URL"))
                continue
            
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
            result = response.json()
            
            if result.get('errcode') == 0:
                results.append((url, True, "✅ 发送成功"))
            else:
                error_msg = result.get('errmsg', '未知错误')
                results.append((url, False, f"❌ 发送失败 (错误码: {result.get('errcode')}): {error_msg}"))
                
        except Exception as e:
            results.append((url, False, f"❌ 发送异常: {str(e)}"))
    
    return results

def get_webhook_urls():
    """获取多个Webhook URL"""
    urls = []
    while True:
        url = input("请输入钉钉机器人Webhook URL（输入空值结束）: ").strip()
        if not url:
            break
        urls.append(url)
    return urls

def main():
    print("="*60)
    print("🚀 钉钉机器人高级消息发送工具")
    print("- 支持文字/图片/图文混合三种模式")
    print("- 支持单机/集群双模式")
    print("- 支持循环发送")
    print("- 支持文字颜色和字号设置")
    print("="*60)
    
    # 选择消息类型
    while True:
        msg_type = input("请选择消息类型:\n1. Markdown文字模式\n2. Markdown图片模式\n3. 图文混合模式\n输入数字(1/2/3): ")
        if msg_type in ['1', '2', '3']:
            break
        print("❌ 输入无效，请输入1、2或3！")
    
    # 选择机器人模式
    while True:
        robot_mode = input("请选择机器人模式:\n1. 多机器人模式（需输入多个Webhook）\n2. 单机器人模式\n输入数字(1/2): ")
        if robot_mode in ['1', '2']:
            break
        print("❌ 输入无效，请输入1或2！")
    
    # 获取基础参数
    if robot_mode == '1':
        webhook_urls = get_webhook_urls()
        if not webhook_urls:
            print("❌ 未输入任何Webhook URL，操作取消")
            return
    else:
        webhook_url = input("请输入钉钉机器人Webhook URL: ").strip()
        webhook_urls = [webhook_url]
    
    # 构建消息负载
    if msg_type == '1':
        # 文字模式
        text = input("请输入Markdown文本内容: ").strip()
        
        # 选择颜色
        while True:
            color_choice = input("请选择文字颜色:\n1. 红色  2. 橙色  3. 黄色  4. 绿色\n5. 蓝色  6. 紫色  7. 白色  8. 黑色\n输入数字(1-8): ")
            if color_choice in COLORS:
                color = COLORS[color_choice]
                break
            print("❌ 输入无效，请输入1-8之间的数字！")
        
        # 选择字号
        while True:
            font_choice = input("请选择字体大小:\n最小  小  中  大  最大\n输入选项: ").strip()
            if font_choice in FONTS:
                font_size = FONTS[font_choice]
                break
            print("❌ 输入无效，请输入有效字号！")
        
        # 应用样式
        styled_text = f"<font color='{color}' size='{font_size}'>{text}</font>"
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "文字消息",
                "text": styled_text
            }
        }
    
    elif msg_type == '2':
        # 图片模式
        image_url = input("请输入图片的公网可访问URL: ").strip()
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "图片消息",
                "text": f"![图片说明]({image_url})"
            }
        }
    
    else:
        # 图文混合模式
        image_url = input("请输入图片的公网可访问URL: ").strip()
        text = input("请输入Markdown文本内容: ").strip()
        
        # 选择颜色
        while True:
            color_choice = input("请选择文字颜色:\n1. 红色  2. 橙色  3. 黄色  4. 绿色\n5. 蓝色  6. 紫色  7. 白色  8. 黑色\n输入数字(1-8): ")
            if color_choice in COLORS:
                color = COLORS[color_choice]
                break
            print("❌ 输入无效，请输入1-8之间的数字！")
        
        # 选择字号
        while True:
            font_choice = input("请选择字体大小:\n最小  小  中  大  最大\n输入选项: ").strip()
            if font_choice in FONTS:
                font_size = FONTS[font_choice]
                break
            print("❌ 输入无效，请输入有效字号！")
        
        # 应用样式
        styled_text = f"<font color='{color}' size='{font_size}'>{text}</font>"
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "图文消息",
                "text": f"![图片说明]({image_url})\n\n{styled_text}"
            }
        }
    
    # 获取循环参数
    while True:
        try:
            loop_count = int(input("请输入发送次数（0表示无限循环）: "))
            interval = float(input("请输入发送间隔（秒）: "))
            if loop_count < 0 or interval < 0:
                raise ValueError
            break
        except ValueError:
            print("❌ 输入无效，请输入非负数值！")
    
    print("-"*60)
    print("开始发送...")
    
    try:
        count = 0
        start_time = time.time()
        
        if loop_count == 0:
            # 无限循环模式
            print("⚠️ 已启动无限循环模式，按Ctrl+C停止")
            while True:
                count += 1
                print(f"\n🔄 第{count}次发送（总耗时: {int(time.time()-start_time)}秒）")
                results = send_dingtalk_markdown(webhook_urls, payload)
                
                for url, success, msg in results:
                    print(f"[{url[:20]}...] {msg}")
                
                time.sleep(interval)
                
        else:
            # 有限次数循环
            for i in range(loop_count):
                count += 1
                print(f"\n🔄 第{count}次发送（剩余: {loop_count - count}次）")
                results = send_dingtalk_markdown(webhook_urls, payload)
                
                for url, success, msg in results:
                    print(f"[{url[:20]}...] {msg}")
                
                time.sleep(interval)
            
            print("✅ 所有消息已发送完毕！")

    except KeyboardInterrupt:
        print("\n🛑 操作已由用户中断")
    except Exception as e:
        print(f"\n❌ 发送过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main()