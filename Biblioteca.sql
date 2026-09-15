CREATE TABLE [vendedores] (
  [id_vendedor] integer PRIMARY KEY,
  [nome] text
)
GO

CREATE TABLE [categorias] (
  [id_categoria] integer PRIMARY KEY,
  [nome] text
)
GO

CREATE TABLE [produtos] (
  [id_produto] integer PRIMARY KEY,
  [nome] text,
  [id_vendedor] integer,
  [id_categoria] integer
)
GO

CREATE TABLE [clientes] (
  [id_cliente] integer PRIMARY KEY,
  [nome] text,
  [email] text,
  [senha] text
)
GO

CREATE TABLE [vendas] (
  [id_venda] integer PRIMARY KEY,
  [id_produto] integer,
  [id_cliente] integer,
  [status] text
)
GO

ALTER TABLE [produtos] ADD FOREIGN KEY ([id_vendedor]) REFERENCES [vendedores] ([id_vendedor])
GO

ALTER TABLE [produtos] ADD FOREIGN KEY ([id_categoria]) REFERENCES [categorias] ([id_categoria])
GO

ALTER TABLE [vendas] ADD FOREIGN KEY ([id_produto]) REFERENCES [produtos] ([id_produto])
GO

ALTER TABLE [vendas] ADD FOREIGN KEY ([id_cliente]) REFERENCES [clientes] ([id_cliente])
GO
