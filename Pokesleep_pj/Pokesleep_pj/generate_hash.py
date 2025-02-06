from werkzeug.security import generate_password_hash, check_password_hash

# パスワードをハッシュ化
password = 'kanri'
hashed_password = generate_password_hash(password, method='scrypt', salt_length=16)
print(f"ハッシュ化されたパスワード: {hashed_password}")

# パスワードの検証
is_correct = check_password_hash(hashed_password, password)
print(f"パスワード検証結果: {is_correct}")
